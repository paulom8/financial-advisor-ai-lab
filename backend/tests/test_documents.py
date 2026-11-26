"""Offline RAG retrieval and provider-contract checks."""

import json
from unittest import TestCase
from unittest.mock import Mock

from test_questions import local_api, model_response
from app.services.document_rag import retrieve


CASES = [
    ("How often does the demo policy review a savings goal?", "savings-goal-review-guide:1"),
    ("Where is the company located?", "company-profile:1"),
    ("How many employees does it have?", "company-profile:2"),
    ("What are its opening hours?", "office-hours-and-contacts:1"),
    ("How long has the company been operating?", "company-profile:3"),
    ("Who is the main contact?", "office-hours-and-contacts:2"),
    ("What AI consulting services are offered?", "ai-consulting-services:1"),
]


def reply(status, answer, citations):
    return model_response({"type": "output_text", "text": json.dumps(
        {"status": status, "answer": answer, "citations": citations}
    )})


class DocumentTests(TestCase):
    def test_retrieval_examples(self):
        for question, expected in CASES:
            with self.subTest(question=question):
                self.assertEqual(retrieve(question)[0].id, expected)
        ids = {p.id for p in retrieve("Who is the main contact, and where is the office?")}
        self.assertTrue({"company-profile:1", "office-hours-and-contacts:2"} <= ids)
        weekend_ids = {p.id for p in retrieve("Can I visit your office on Saturday, and who should I contact?")}
        self.assertTrue({"office-hours-and-contacts:1", "office-hours-and-contacts:2"} <= weekend_ids)
        self.assertTrue(retrieve("Is there a fee for changing a goal?"))
        self.assertEqual(retrieve("volcanoes"), [])

    def test_retrieval_only_and_empty_match_never_call_provider(self):
        provider = Mock(side_effect=AssertionError("Unexpected model call"))
        with local_api(provider) as api:
            response = api.post("/api/documents/retrieve", json={"question": CASES[0][0]})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["passages"][0]["id"], CASES[0][1])
            response = api.post("/api/documents/ask", json={"question": "volcanoes"})
            self.assertEqual(response.json()["status"], "not_covered")
            self.assertFalse(response.json()["model_called"])
        provider.assert_not_called()

    def test_grounded_response_and_provider_context(self):
        question = "Who is the main contact, and where is the office?"
        ids = ["office-hours-and-contacts:2", "company-profile:1"]
        provider = Mock(return_value=reply("answered", "Paulo Umetsu, CEO and Owner, at the Asquith office.", ids))
        with local_api(provider) as api:
            result = api.post("/api/documents/ask", json={"question": question}).json()
        self.assertEqual(result["status"], "answered")
        self.assertEqual(result["citations"], ids)
        request = json.loads(provider.call_args.args[0].content)
        self.assertFalse(request["store"])
        self.assertNotIn("tools", request)
        data = json.loads(request["input"])
        self.assertEqual(data["question"], question)
        self.assertEqual(data["passages"], [{k: v for k, v in p.items() if k != "score"} for p in result["passages"]])
        self.assertLessEqual(len(data["passages"]), 3)

    def test_unsupported_fee_and_invalid_citation(self):
        provider = Mock(side_effect=[
            reply("not_covered", "unsupported", []),
            reply("answered", "made up", ["nonexistent:1"]),
        ])
        with local_api(provider) as api:
            result = api.post("/api/documents/ask", json={"question": "Is there a fee for changing a goal?"}).json()
            self.assertEqual(result["status"], "not_covered")
            self.assertEqual(result["answer"], "The documents don't cover this question.")
            self.assertEqual(result["citations"], [])
            result = api.post("/api/documents/ask", json={"question": CASES[0][0]}).json()
            self.assertEqual(result["status"], "error")
            self.assertTrue(result["passages"])

class DirectDocumentTests(TestCase):
    """Check the model contract without creating an event loop or network socket."""

    def test_generation_contract(self):
        from types import SimpleNamespace
        from unittest.mock import AsyncMock
        from app.services.document_rag import generate
        from app.services.openai_service import OpenAIServiceError

        def complete(coroutine):
            try:
                coroutine.send(None)
            except StopIteration as stop:
                return stop.value
            self.fail("Mock unexpectedly suspended")

        question = "Who is the main contact, and where is the office?"
        passages = retrieve(question)
        ids = ["office-hours-and-contacts:2", "company-profile:1"]
        create = AsyncMock(return_value=SimpleNamespace(
            status="completed", output_text=json.dumps({
                "status": "answered", "answer": "Paulo Umetsu, CEO and Owner, at the Asquith office.",
                "citations": ids,
            })
        ))
        client = SimpleNamespace(responses=SimpleNamespace(create=create))
        answer, called = complete(generate(question, passages, client))
        self.assertTrue(called)
        self.assertEqual(answer.citations, ids)
        kwargs = create.call_args.kwargs
        self.assertFalse(kwargs["store"])
        self.assertEqual(json.loads(kwargs["input"])["passages"],
                         [p.model_dump(exclude={"score"}) for p in passages])
        create.return_value.output_text = json.dumps({"status": "not_covered", "answer": "unsupported", "citations": []})
        answer, called = complete(generate("Is there a fee for changing a goal?", retrieve("Is there a fee for changing a goal?"), client))
        self.assertEqual(answer.answer, "The documents don't cover this question.")
        create.return_value.output_text = json.dumps({"status": "answered", "answer": "invented", "citations": ["invalid"]})
        with self.assertRaises(OpenAIServiceError):
            complete(generate(question, passages, client))
        create.reset_mock()
        answer, called = complete(generate("volcanoes", [], client))
        self.assertFalse(called)
        self.assertEqual(answer.status, "not_covered")
        create.assert_not_called()
