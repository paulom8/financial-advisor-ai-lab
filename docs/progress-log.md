# Project progress

This log records what has been completed, what is current, and what remains to explore. The [learning roadmap](learning-roadmap.md) is the source of truth for the full industry-prioritized category list and its statuses.

## Completed foundation

- **Git and GitHub repository integration:** the project is connected to its remote repository and uses the documented feature-branch workflow.
- **PostgreSQL sample database:** the `financial_advisor_lab` database and `Test` sample-record table are in use.
- **API and database integration:** FastAPI serves rows from PostgreSQL through `GET /api/test-records`.
- **React page integration:** the first page displayed sample records from FastAPI, completing the React → FastAPI → PostgreSQL path.
- **Focused endpoint verification:** `GET /api/test-records` returned HTTP 200 with the expected synthetic record fields and ascending ID order.

These are supporting application foundations. The database and API work is not a programming curriculum; it provides a place to explore AI capabilities in an application.

## Completed AI experiment

**Single-turn question and answer using OpenAI — Completed, 20 November 2026.** The user reviewed the response in the React page and traced how the synthetic question reached OpenAI through FastAPI. The backend holds the API key and sends each question independently through the Responses API.

During the feature review, six backend tests and seven frontend tests passed, the frontend built successfully, and a live browser submission displayed the expected answer to a fictional arithmetic question. The offline tests covered validation, rejected keys, provider failures, and unexpected response formats.

## Current focus

The next experiment is open. Use the [roadmap's priority baseline](learning-roadmap.md#industry-prioritised-categories) to choose the next learning question.

## Still to explore

The roadmap tracks the remaining areas, including AI application architecture and deployment; MCP, connectors, and plugins; model evaluation and observability; security and governance; function calling; prompts; workflows; context and retrieval; multimodal inputs and outputs; assistants; reusable AI components; and agents.

Update this log when a meaningful milestone is completed or the current focus changes. Keep claims aligned with work that has actually been tried and reviewed.
