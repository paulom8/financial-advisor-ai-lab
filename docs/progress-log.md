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

**Edited targets follow-up, 22 November 2026.** The original filter excluded a demo record when its amount changed. The tool now checks the approved client and goal separately from the numeric target. The seed command preserves edited amounts. All 13 backend tests passed, and a live question returned Demo Client B at AUD $85,000 from the edited PostgreSQL record.

## Current focus

**Model evaluation — In progress, 22 November 2026.** The separate **Evaluate the model** page scores the largest savings target, an absent client, and a general compound interest question. It checks tool use and the answer independently. The user can edit a fictional target and rerun the evaluation against the current records.

Verification passed with 18 backend tests, nine frontend tests, and a frontend production build. A browser run used local PostgreSQL and simulated provider replies to show separate failures for a wrong amount and a missing lookup, and a pass for the general question. The first live evaluation is pending user review.

**Plain-text RAG - Completed (26 November 2026).** Approved temporary detour building on database lookup and evaluation. The Ask the documents page uses four fictional company documents, shows ranked passages and citations independently of generation, and retains newest-first results during the page session. Retrieval-only is independent of OpenAI. Unsupported questions offer a fictional contact-email link. Embeddings and vector databases are deferred. Offline retrieval and direct mocked generation checks passed; 11 frontend tests and the production build passed. The full backend TestClient suite could not run in the restricted Windows environment because event-loop socket initialization stalled. A user live question about visiting on Saturday and contacting the office exposed a lexical retrieval gap: Saturday did not match weekends. Added weekend synonym normalization and a retrieval regression case. User live review confirmed correct answers and citations for Sunday and after 8 pm, with both opening hours and main contact retrieved. The keyword experiment is complete; full backend integration checks and the broader live question set were not verified. Next approved experiment: embeddings and semantic similarity.

**Embeddings and semantic similarity - Completed (26 November 2026).** The document page can compare keyword and semantic rankings for one question across the same sections. OpenAI embeds the question and sections in a single request, and Python ranks the passages by cosine similarity. The user confirmed that semantic search found the Operating history passage for "How long has the company been in the market?" The passage states 10 years as of 26 November 2026.

**Vector databases - In progress.** pgvector 0.8.7 is enabled in PostgreSQL 18. The user seeded nine fictional passages with 1,536-dimensional embeddings. The document page can embed a new question and rank saved passages in PostgreSQL. Live review of the new search is pending.

**RAG evaluation - In progress.** The documents page runs a direct employee question, a paraphrase and an unsupported fee question through keyword and saved-vector retrieval and the same model answer path. It checks retrieval and answers independently and displays the supporting citations. Live review is pending.

## Still to explore

The roadmap tracks the remaining areas, including AI application architecture and deployment; MCP, connectors, and plugins; model evaluation and observability; security and governance; prompts; workflows; context and retrieval; multimodal inputs and outputs; assistants; reusable AI components; and agents.

Update this log when a meaningful milestone is completed or the current focus changes. Keep claims aligned with work that has actually been tried and reviewed.
