# Project progress

This log records what has been completed, what is current, and what remains to explore. The [learning roadmap](learning-roadmap.md) is the source of truth for the full industry-prioritized category list and its statuses.

## Completed foundation

- **Git and GitHub repository integration:** the project is connected to its remote repository and uses the documented feature-branch workflow.
- **PostgreSQL sample database:** the `financial_advisor_lab` database and `Test` sample-record table are in use.
- **API and database integration:** FastAPI serves rows from PostgreSQL through `GET /api/test-records`.
- **React page integration:** the first page displayed sample records from FastAPI, completing the React → FastAPI → PostgreSQL path.
- **Focused endpoint verification:** `GET /api/test-records` returned HTTP 200 with the expected synthetic record fields and ascending ID order.

These are supporting application foundations. The database and API work is not a programming curriculum; it provides a place to explore AI capabilities in an application.

## Completed AI experiments

**Single-turn question and answer using OpenAI — Completed, 20 November 2026.** The user reviewed the response in the React page and traced how the synthetic question reached OpenAI through FastAPI. The backend holds the API key and sends each question independently through the Responses API.

During the feature review, six backend tests and seven frontend tests passed, the frontend built successfully, and a live browser submission displayed the expected answer to a fictional arithmetic question. The offline tests covered validation, rejected keys, provider failures, and unexpected response formats.

**Function calling with fictional PostgreSQL records — Completed, 22 November 2026.** The implementation exposes one bounded, read-only `list_test_records` function to OpenAI and returns its result for a final answer. The explicit seed command added five fictional examples and zero rows on the repeat run. The initial live examples covered the saved goals, largest target, absent client, and general answer paths. The React page displayed a grounded database answer and the function-use badge.

The code review restricted the tool to the five approved descriptions, moved the database read to a worker thread, and tightened validation and stateless replay. The updated checks passed (11 backend tests, seven frontend tests, and the frontend build). A live PostgreSQL check confirmed five approved tool descriptions and six rows on the separate records endpoint. Live OpenAI calls confirmed the largest-target question used the function and the compound-interest question answered directly.

The user approved integration after the implementation review and walkthrough.

## Still to explore

The roadmap tracks the remaining areas, including AI application architecture and deployment; MCP, connectors, and plugins; model evaluation and observability; security and governance; prompts; workflows; context and retrieval; multimodal inputs and outputs; assistants; reusable AI components; and agents.

Update this log when a meaningful milestone is completed or the current focus changes. Keep claims aligned with work that has actually been tried and reviewed.
