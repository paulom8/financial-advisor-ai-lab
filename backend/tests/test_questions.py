"""Exercise the question endpoint without local credentials, PostgreSQL, or a network."""

import json
import os
from contextlib import contextmanager
from unittest import TestCase
from unittest.mock import Mock, patch

import httpx
from fastapi.testclient import TestClient
from openai import AsyncOpenAI

# Configuration loads at import time. Give the app only synthetic test settings.
with patch("dotenv.load_dotenv"), patch.dict(os.environ, {}, clear=True):
    from app import main


def model_response(*content, status="completed", incomplete_details=None):
    return httpx.Response(200, json={
        "id": "resp_synthetic",
        "object": "response",
        "status": status,
        "incomplete_details": incomplete_details,
        "output": [{"type": "message", "role": "assistant", "content": list(content)}],
    })


@contextmanager
def local_api(handler, *, api_key="test-key"):
    def create_sdk_client(**kwargs):
        http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler), trust_env=False)
        return AsyncOpenAI(base_url="https://provider.invalid/v1", http_client=http_client, **kwargs)

    with (
        patch.object(main, "OPENAI_API_KEY", api_key),
        patch.object(main, "AsyncOpenAI", side_effect=create_sdk_client),
        patch.object(main, "initialize_sample_table"),
        patch.object(main.engine, "connect", side_effect=AssertionError("Unexpected database access")),
        TestClient(main.app) as api,
    ):
        yield api


class QuestionEndpointTests(TestCase):
    def test_successful_request_is_trimmed_and_stateless(self):
        provider = Mock(return_value=model_response({"type": "output_text", "text": " Four. "}))
        with local_api(provider) as api:
            response = api.post("/api/ask", json={"question": "  What is two plus two? "})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"answer": "Four."})
        provider.assert_called_once()
        request = provider.call_args.args[0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.url.path, "/v1/responses")
        body = json.loads(request.content)
        self.assertEqual(body["input"], "What is two plus two?")
        self.assertIs(body["store"], False)
        self.assertNotIn("previous_response_id", body)

    def test_invalid_questions_do_not_reach_provider(self):
        provider = Mock()
        with local_api(provider) as api:
            for invalid in ({}, {"question": "  "}, {"question": "a" * 4001}):
                with self.subTest(length=len(invalid.get("question", ""))):
                    self.assertEqual(api.post("/api/ask", json=invalid).status_code, 422)
        provider.assert_not_called()

    def test_missing_key_does_not_reach_provider(self):
        provider = Mock()
        with local_api(provider, api_key="") as api:
            response = api.post("/api/ask", json={"question": "What is a fictional budget?"})
        self.assertEqual(response.status_code, 503)
        self.assertIn("not configured", response.json()["detail"])
        provider.assert_not_called()

    def test_provider_errors_explain_the_problem_without_echoing_provider_details(self):
        for status, code, expected, message in (
            (401, "invalid_api_key", 503, "rejected the backend API key"),
            (404, "model_not_found", 503, "OPENAI_MODEL"),
            (429, "insufficient_quota", 503, "insufficient quota"),
            (429, "rate_limit_exceeded", 429, "rate limit"),
            (500, "server_error", 502, "could not complete"),
        ):
            with self.subTest(code=code):
                raw_detail = "synthetic provider diagnostic for internal use"
                provider = Mock(return_value=httpx.Response(status, json={
                    "error": {"code": code, "message": raw_detail},
                }))
                with local_api(provider) as api:
                    response = api.post("/api/ask", json={"question": "Explain a test budget."})
                self.assertEqual(response.status_code, expected)
                self.assertIn(message, response.json()["detail"])
                self.assertNotIn(raw_detail, response.text)
                provider.assert_called_once()

    def test_timeout_is_reported_without_replaying_the_request(self):
        provider = Mock(side_effect=httpx.ReadTimeout("simulated timeout"))
        with local_api(provider) as api:
            response = api.post("/api/ask", json={"question": "Explain simple interest."})
        self.assertEqual(response.status_code, 504)
        provider.assert_called_once()

    def test_refusal_is_readable_and_partial_output_is_never_shown_as_complete(self):
        provider = Mock(side_effect=[
            model_response({"type": "refusal", "refusal": "I can only provide general information."}),
            model_response({"type": "output_text", "text": "A partial sentence"},
                           status="incomplete", incomplete_details={"reason": "max_output_tokens"}),
        ])
        with local_api(provider) as api:
            question = {"question": "Explain a fictional savings goal."}
            refusal = api.post("/api/ask", json=question)
            incomplete = api.post("/api/ask", json=question)
        self.assertEqual(refusal.status_code, 200)
        self.assertEqual(refusal.json(), {"answer": "I can only provide general information."})
        self.assertEqual(incomplete.status_code, 502)
        self.assertIn("output limit", incomplete.json()["detail"])
        self.assertNotIn("A partial sentence", incomplete.text)
