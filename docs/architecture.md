# Architecture

This document distinguishes the user's stated direction from architectural recommendations. A proposed choice is not a permanent commitment until the user approves it for implementation.

## Confirmed direction

The user proposed the following stack and direction:

- Frontend: React.
- Backend: Python FastAPI.
- Database: PostgreSQL.
- Version control: Git and GitHub.
- Docker and cloud hosting may be explored later; local development comes first.
- AI provider choice is open. OpenAI, Anthropic, and Google were suggested as possible providers, but using all three is not required.
- The system should eventually support experiments comparing models and possibly provider fallback, but these are learning goals, not first-version requirements.
- For the first implementation, build a simple React page, a Python FastAPI backend, and a PostgreSQL database. Use a database named `financial_advisor_lab`, with a `Test` table containing an integer incrementing `id`, `description` (`varchar(255)`), and `date_inserted` (`datetime`). Seed one synthetic record and display all records on the page.
- SQLAlchemy is selected for this small database experiment. The API initializes the table and inserts the sample record only when the table is empty.
- Use Vite and npm for the initial React page.
- The backend connects with a dedicated `financial_advisor_app` login role, separate from the PostgreSQL `postgres` administrator account. Keep its password in the ignored local environment file; the role owns only the `financial_advisor_lab` database.

## Proposed architecture

Start as a **modular monolith**, growing only when an experiment needs another component:

```text
React user interface
        │ HTTP API
        ▼
FastAPI application
  ├─ Advisor/client workflow
  ├─ Deterministic validation and business rules
  ├─ AI integration and versioned prompts (when introduced)
  ├─ Explicitly allowlisted tool execution (when introduced)
  ├─ Document processing and retrieval (later experiments)
  └─ Evaluation and usage records (as needed)
        │
        ├─ PostgreSQL (when persistence is useful)
        └─ One or more model APIs (when AI experiments need them)
```

This keeps the eventual shape understandable without requiring every component at the start. The initial experiment could be even smaller (for example, static text in the UI); no first feature or implementation sequence has yet been approved.

## Design recommendations

- Keep basic data validation and repeatable rules in application code. Ask models to identify possible inconsistencies or suggest questions, and present those as reviewable suggestions.
- When AI is introduced, keep API credentials on the backend, validate model outputs, handle provider failures, and record enough metadata to understand experiments.
- Add a provider interface when a second provider or meaningful provider comparison is needed. Avoid a broad abstraction before provider differences matter.
- Keep model requests and tools bounded. Validate tool arguments, enforce an allowlist, and require advisor confirmation for consequential writes.
- Add persistence when saving clients, conversations, documents, or experiment results becomes useful. Use migrations when a database is introduced.
- Add document ingestion and retrieval only when a learning experiment calls for them; retain source references for extracted or retrieved content.
- Keep multi-agent workflows, deployment, and infrastructure expansion late and justified.

## Dependency outline (proposed)

```text
React screen ──► API endpoint ──► model API
                       │
                       ├─► deterministic rules
                       ├─► PostgreSQL persistence (when needed)
                       ├─► tool execution (after API/model basics)
                       ├─► document extraction ──► retrieval/RAG
                       └─► logs/evaluations (introduced early in small form,
                                            expanded with experiments)
```

Likely prerequisites: basic API calls precede provider comparison; model interaction and schemas precede robust tool loops; document extraction precedes retrieval over documents; tests and evaluation cases should grow alongside features rather than being postponed entirely. These are recommendations and may be adjusted with an explained roadmap detour.

## Open questions

- Which provider and model should power the first AI experiment, if any?
- Which frontend build setup should be used as the React experiment grows?
- What local development environment and container workflow should be adopted?
- Which evaluation, logging, and privacy controls are appropriate for each experiment?
- What hosting target, if any, should eventually be explored?

Resolve these when they become relevant; do not invent answers in advance.
