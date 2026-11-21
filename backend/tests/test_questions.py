"""Exercise the question endpoint without local credentials, PostgreSQL, or a network."""

import json
import os
from contextlib import contextmanager
from unittest import TestCase
from unittest.mock import Mock, patch

import httpx
from fastapi.testclient import TestClient
from openai import AsyncOpenAI
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configuration loads at import time. Give the app only synthetic test settings.
with patch("dotenv.load_dotenv"), patch.dict(os.environ, {}, clear=True):
    from app import main
    from app.models import TestRecord
    from app.services.test_record_service import SYNTHETIC_RECORDS
    from app.services.test_record_tool import MAX_TOOL_RECORDS


def model_response(*content, status="completed", incomplete_details=None):
    return httpx.Response(200, json={
        "id": "resp_synthetic",
        "object": "response",
        "status": status,
        "incomplete_details": incomplete_details,
        "output": [{"type": "message", "role": "assistant", "content": list(content)}],
    })


def function_call(**overrides):
    return {
        "type": "function_call",
        "id": "fc_synthetic",
        "call_id": "call_synthetic",
        "name": "list_test_records",
        "arguments": "{}",
        "status": "completed",
        **overrides,
    }


def tool_response(*items, status="completed"):
    return httpx.Response(200, json={
        "id": "resp_function_call",
        "object": "response",
        "status": status,
        "output": list(items),
    })


@contextmanager
def local_api(handler, *, api_key="test-key"):
    def create_sdk_client(**kwargs):
        http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler), trust_env=False)
        return AsyncOpenAI(base_url="https://provider.invalid/v1", http_client=http_client, **kwargs)

    with (
        patch.object(main, "OPENAI_API_KEY", api_key),
        patch.object(main, "AsyncOpenAI", side_effect=create_sdk_client),
        patch.object(main, "initialize_test_table"),
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
        self.assertEqual(response.json(), {"answer": "Four.", "database_function_used": False})
        provider.assert_called_once()
        request = provider.call_args.args[0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.url.path, "/v1/responses")
        body = json.loads(request.content)
        self.assertEqual(body["input"], "What is two plus two?")
        self.assertIs(body["store"], False)
        self.assertEqual(body["tools"][0]["name"], "list_test_records")
        self.assertEqual(body["tool_choice"], "auto")
        self.assertIs(body["parallel_tool_calls"], False)
        self.assertNotIn("previous_response_id", body)

    def test_function_call_round_trip_returns_result_and_preserves_response_items(self):
        records = {
            "limit": 50,
            "truncated": False,
            "records": [SYNTHETIC_RECORDS[2]],
        }
        reasoning = {
            "type": "reasoning",
            "id": "rs_synthetic",
            "summary": [],
            "encrypted_content": "synthetic-encrypted-content",
        }
        call = function_call()
        provider = Mock(side_effect=[
            tool_response(reasoning, call),
            model_response({"type": "output_text", "text": "Demo Client C has the largest target at AUD $42,000."}),
        ])
        with local_api(provider) as api, patch(
            "app.api.routes.questions.list_test_records_for_tool", return_value=records
        ) as read_records:
            response = api.post("/api/ask", json={"question": "Which client has the largest target?"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "answer": "Demo Client C has the largest target at AUD $42,000.",
            "database_function_used": True,
        })
        read_records.assert_called_once_with()
        self.assertEqual(provider.call_count, 2)
        first_body = json.loads(provider.call_args_list[0].args[0].content)
        self.assertIs(first_body["store"], False)
        self.assertEqual(first_body["include"], ["reasoning.encrypted_content"])
        second_body = json.loads(provider.call_args_list[1].args[0].content)
        self.assertIs(second_body["store"], False)
        self.assertNotIn("previous_response_id", second_body)
        self.assertEqual(second_body["tool_choice"], "none")
        self.assertEqual(second_body["input"][0]["content"], "Which client has the largest target?")
        self.assertEqual(second_body["input"][1:3], [reasoning, call])
        result = second_body["input"][3]
        self.assertEqual(result["type"], "function_call_output")
        self.assertEqual(result["call_id"], call["call_id"])
        self.assertEqual(json.loads(result["output"]), records)

    def test_invalid_or_incomplete_function_calls_never_read_database(self):
        for response_from_provider in (
            tool_response(function_call(name="write_records")),
            tool_response(function_call(namespace="another_tool")),
            tool_response(function_call(arguments='{"limit": 500}')),
            tool_response(function_call(arguments="[]")),
            tool_response(function_call(arguments="{")),
            tool_response(function_call(call_id="")),
            tool_response({key: value for key, value in function_call().items() if key != "call_id"}),
            tool_response(function_call(status="incomplete")),
            tool_response(function_call(), status="incomplete"),
            tool_response(function_call(), function_call(call_id="call_second")),
        ):
            with self.subTest(response=response_from_provider.json()):
                provider = Mock(return_value=response_from_provider)
                with local_api(provider) as api, patch(
                    "app.api.routes.questions.list_test_records_for_tool"
                ) as read_records:
                    response = api.post("/api/ask", json={"question": "Read the saved records."})
                self.assertEqual(response.status_code, 502)
                read_records.assert_not_called()
                provider.assert_called_once()

    def test_database_function_failure_returns_clear_error(self):
        provider = Mock(return_value=tool_response(function_call()))
        with local_api(provider) as api, patch(
            "app.api.routes.questions.list_test_records_for_tool",
            side_effect=SQLAlchemyError("private database details"),
        ):
            response = api.post("/api/ask", json={"question": "List the saved records."})
        self.assertEqual(response.status_code, 503)
        self.assertIn("database function could not read", response.json()["detail"])
        self.assertNotIn("private database details", response.text)
        provider.assert_called_once()

    def test_follow_up_cannot_run_the_tool_again(self):
        provider = Mock(side_effect=[
            tool_response(function_call()),
            tool_response(function_call(call_id="call_second")),
        ])
        with local_api(provider) as api, patch(
            "app.api.routes.questions.list_test_records_for_tool",
            return_value={"limit": 50, "truncated": False, "records": []},
        ) as read_records:
            response = api.post("/api/ask", json={"question": "List the saved records."})

        self.assertEqual(response.status_code, 502)
        read_records.assert_called_once_with()
        self.assertEqual(provider.call_count, 2)

    def test_provider_only_receives_approved_descriptions_and_page_gets_limit_notice(self):
        engine = create_engine(
            "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
        )
        self.addCleanup(engine.dispose)
        TestRecord.__table__.create(engine)
        sessions = sessionmaker(bind=engine)
        unapproved = "FICTIONAL DEMO — An unapproved test description"
        with sessions.begin() as db:
            db.add(TestRecord(description=unapproved))
            db.add_all(
                TestRecord(description=SYNTHETIC_RECORDS[i % len(SYNTHETIC_RECORDS)])
                for i in range(MAX_TOOL_RECORDS + 1)
            )

        provider = Mock(side_effect=[
            tool_response(function_call()),
            model_response({"type": "output_text", "text": "Here are the matching goals."}),
        ])
        with local_api(provider) as api, patch(
            "app.services.test_record_tool.SessionLocal", sessions
        ):
            response = api.post("/api/ask", json={"question": "List the saved records."})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["database_function_used"])
        self.assertIn(
            f"only the first {MAX_TOOL_RECORDS} matching fictional rows", response.json()["answer"]
        )
        sent = json.loads(provider.call_args_list[1].args[0].content)
        result = json.loads(sent["input"][-1]["output"])
        self.assertTrue(result["truncated"])
        self.assertEqual(len(result["records"]), MAX_TOOL_RECORDS)
        self.assertEqual(set(result["records"]), set(SYNTHETIC_RECORDS))

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
        self.assertEqual(refusal.json(), {
            "answer": "I can only provide general information.",
            "database_function_used": False,
        })
        self.assertEqual(incomplete.status_code, 502)
        self.assertIn("output limit", incomplete.json()["detail"])
        self.assertNotIn("A partial sentence", incomplete.text)
