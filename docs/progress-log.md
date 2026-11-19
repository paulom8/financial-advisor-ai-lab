# Project progress

This log records what has been completed, what is current, and what remains to explore. The [learning roadmap](learning-roadmap.md) is the source of truth for the full industry-prioritized category list and its statuses.

## Completed foundation

- **Git and GitHub repository integration:** the project is connected to its remote repository and uses the documented feature-branch workflow.
- **PostgreSQL sample database:** the `financial_advisor_lab` database and `Test` sample-record table are in use.
- **API and database integration:** FastAPI serves rows from PostgreSQL through `GET /api/test-records`.
- **React page integration:** the page displays the API response, completing the React → FastAPI → PostgreSQL path.
- **Focused endpoint verification:** `GET /api/test-records` returned HTTP 200 with the expected synthetic record fields and ascending ID order.

These are supporting application foundations. The database and API work is not a programming curriculum; it provides a place to explore AI capabilities in an application.

## Current focus

**Single-turn AI question and answer using OpenAI — In progress; implementation not started.** The proposed slice is a text box and submit button that sends one question through the backend to OpenAI and displays the answer. The API key must stay in a local backend environment file and out of browser code and Git. Use synthetic, non-sensitive example questions.

This slice is intended to explore a model API integration and basic text interaction. After inspecting it, the next small experiment can be chosen from the roadmap.

## Still to explore

The roadmap tracks the remaining areas, including AI application architecture and deployment; SDKs, MCP, connectors, and plugins; evaluation and observability; security and governance; function calling; prompts; workflows; context and retrieval; multimodal inputs and outputs; assistants; reusable AI components; and agents.

Update this log when a meaningful milestone is completed or the current focus changes. Keep claims aligned with work that has actually been tried and reviewed.
