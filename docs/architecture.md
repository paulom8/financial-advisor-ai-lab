# Architecture

This document distinguishes confirmed direction, current implementation, and proposals. The application is a learning environment for AI capabilities and their use in real applications. Keep architecture purposeful: use it to make an experiment work, not as a separate programming curriculum.

## Confirmed direction

- Frontend: React.
- Backend: Python FastAPI.
- Database: PostgreSQL.
- Version control: Git and GitHub.
- Use local development first. Docker and cloud hosting may be explored later when they support a learning objective.
- Use OpenAI for the single-question text experiment. Provider and model choices for future experiments remain open.
- The system may eventually support experiments comparing models or providers. Add comparison or fallback behavior only when a concrete learning question makes it useful.
- Use synthetic data only. Keep secrets on the backend when a provider API is connected.

## Current implementation

The React pages use Vite and npm. FastAPI exposes the following experiment routes.

| FastAPI route | Request and result | External dependency |
|---|---|---|
| `POST /api/ask` | The React form submits `{"question": "..."}`. FastAPI validates it and returns an answer plus `database_function_used` for human review. | The backend calls the OpenAI Responses API using the official Python SDK and may execute the single allowlisted database function. |
| `GET /api/test-records` | Returns the sample rows from the introductory database experiment. | SQLAlchemy reads the PostgreSQL `"Test"` table. |
| `POST /api/evaluation` | The evaluation page sends `{"run": true}` and displays the expected answer, actual answer, tool use, and verdict for each of three preset questions. | FastAPI reads the approved PostgreSQL records once and uses the existing OpenAI question flow. |

| `POST /api/documents/retrieve` | Ranks plain-text sections and returns up to three passages with scores. | Local files only. |
| `POST /api/documents/ask` | Retrieves the same passages and returns an answer, citation IDs, status and passages. | OpenAI (only when passages match). |

Each submission sends one independent question. FastAPI reuses its OpenAI client across requests and sets `store=False` for both Responses API calls. Questions and answers stay out of PostgreSQL. The backend reads `OPENAI_API_KEY` and the optional `OPENAI_MODEL` at startup. The ignored backend environment file holds local credentials. See the [local setup instructions](../README.md#run-locally).

The dedicated `financial_advisor_app` role owns the `financial_advisor_lab` database. The `Test` table has an incrementing integer `id`, a `description` of up to 255 characters, and a `date_inserted` timestamp. Startup creates the table if needed, but does not insert rows. The explicit `python -m app.seed_test_records` command adds the missing examples from the five labelled fictional client and goal pairs. It preserves edited amounts and other rows.

The question route exposes one strict `list_test_records` function with no arguments. FastAPI accepts a single completed call with the expected name, a call ID, and an empty JSON object. It runs the synchronous SQLAlchemy query in a worker thread. The query selects descriptions containing an approved fictional client and goal followed by a valid numeric AUD amount. The amount comes from PostgreSQL on each lookup. FastAPI checks the full description again before sending it to OpenAI. It reads up to 51 matching rows in ascending ID order, sends the first 50, and adds a notice to the answer if more rows matched.

The follow-up request sends the original question, the first response’s output items (including encrypted reasoning when available), and the function result paired with its call ID. Response storage stays disabled on both requests, and the follow-up disables further calls. The model is instructed to ground record claims in the returned descriptions. React uses `database_function_used` to show whether the query ran. The direct question flow and the separate records endpoint remain available.

An evaluation run validates that its snapshot contains one record for each approved demo client and computes the expected largest target from the saved amounts. The model sees that same snapshot when it requests the function. Each of the three questions starts independently. Application rules check whether the model chose the expected tool and answered in the requested format. A provider error appears separately from an incorrect answer. The run starts only on request, uses at most six OpenAI calls, and keeps its report in the current page.

The approved RAG detour uses four synthetic text files in backend/app/documents. Headings define passage boundaries; a deterministic keyword overlap score weights headings twice as much as body text, with simple normalization and a three-passage limit. No embeddings, vector database, uploads or new dependencies. Retrieval-only does not call a model. Generation uses the existing SDK client without database tools or conversation history, sends only the question and retrieved passages, requests structured answer status and source IDs, and validates that citations refer to retrieved passages. It does not prove factual faithfulness; compare the answer against the displayed sources. Empty retrieval abstains locally; insufficient evidence after retrieval requires model abstention. Provider failures remain separate. The page retains question results newest-first in memory and offers a fictional contact email link for unsupported questions; it does not send email.

## Proposed architecture

The proposed direction is a simple modular monolith, growing only when an experiment needs another component:

```text
React learning page
        │
        ▼
FastAPI application ──► Model API / SDK
        │                    │
        ├─► PostgreSQL        └─► model capabilities
        ├─► connectors, plugins, or MCP (when useful)
        └─► bounded tool execution (when explored)
```

Future experiments may compare model outputs or connect the existing FastAPI application to additional services. Application logic should handle secrets, validate structured outputs, and control any tool execution. Add persistence only if saving synthetic experiments is useful. This is a proposed shape, not a requirement to build every component.

Relevant integration learning includes:

- Calling model APIs and using provider SDKs.
- Connecting external tools and services through APIs, connectors, or plugins.
- Exploring MCP as an integration protocol when it supports a concrete experiment.
- Comparing direct model calls, reusable provider features, and application-managed behavior.

These are important parts of the learning roadmap, but do not build every integration layer in advance. Choose tools and patterns based on practical industry use and the experiment's purpose.

## Design guidance

- Keep deterministic application rules separate from model suggestions. Show suggestions as reviewable, not verified facts.
- When using an AI API, keep credentials out of the browser and repository, validate inputs/outputs, and handle provider errors.
- Introduce an abstraction only when provider comparison or a real code need justifies it.
- For tool use, define a narrow allowlist, validate arguments, and keep consequential actions under human control.
- Choose evaluation metadata that helps explain model behavior while protecting question and answer content.
- Introduce migrations when an approved experiment changes an existing schema and needs to preserve data.
- Add document extraction before retrieval over documents; retain source references when AI answers rely on sources.
- Multi-agent workflows, deployment, and infrastructure expansion should have a clear learning reason. They are not required architecture milestones.

## Open questions

- Which capability should the next experiment explore?
- Which model/provider and access path best fit that capability and its industry use?
- Should the experiment run in this page, a provider interface, or both for comparison?
- Which API, SDK, connector, plugin, or MCP integration is relevant to the chosen experiment?
- What evaluation, logging, privacy, and deployment choices would the experiment require?

Resolve these questions as they become relevant; keep proposals distinct from confirmed decisions.
