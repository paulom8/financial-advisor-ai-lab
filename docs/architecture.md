# Architecture

This document distinguishes the user's stated direction from architectural recommendations. A proposed choice is not a permanent commitment until the user approves it for implementation.

## Confirmed direction

Development takes place locally using React, Vite and npm for the frontend, FastAPI for the backend, and Git and GitHub for version control.

| FastAPI route | Request and result | External dependency |
|---|---|---|
| `POST /api/ask` | The React form submits `{"question": "..."}`. FastAPI validates it and returns `{"answer": "..."}` to the same page. | The backend calls the OpenAI Responses API using the official Python SDK. |
| `GET /api/test-records` | Returns the records used in the introductory database experiment. | SQLAlchemy reads the PostgreSQL `"Test"` table. |

Each submission sends one independent question. FastAPI reuses its OpenAI client across requests and sets `store=False` to disable storage of the response for later retrieval through the Responses API. Questions and answers stay out of PostgreSQL. The backend reads `OPENAI_API_KEY` and the optional `OPENAI_MODEL` when it starts. The ignored backend environment file holds local credentials. See the [local setup instructions](../README.md#run-locally).

The dedicated `financial_advisor_app` role owns the `financial_advisor_lab` database. The sample table has an incrementing integer `id`, a `description` of up to 255 characters, and a `date_inserted` timestamp. The API initializes the table and seeds a synthetic record when it is empty.

## Proposed architecture

Keep future advisor workflows, validation and provider calls in the same FastAPI application as long as that structure serves the experiments. Model comparisons and provider fallback remain possible learning exercises. Additional providers, deployment and the order of future experiments remain open.

## Design recommendations

- Keep basic data validation and repeatable rules in application code. Ask models to identify possible inconsistencies or suggest questions, and present those as reviewable suggestions.
- For future evaluation experiments, decide which metadata helps explain model behaviour while protecting question and answer content.
- Add a provider interface when a second provider or meaningful provider comparison is needed. Avoid a broad abstraction before provider differences matter.
- Keep model requests and tools bounded. Validate tool arguments, enforce an allowlist, and require advisor confirmation for consequential writes.
- Introduce migrations when an experiment changes an existing schema and needs to preserve its data. Add tables for clients, conversations, documents or results only when an approved feature needs them.
- Add document ingestion and retrieval only when a learning experiment calls for them; retain source references for extracted or retrieved content.
- Keep multi-agent workflows, deployment, and infrastructure expansion late and justified.

## Open questions

- Which frontend build setup should be used as the React experiment grows?
- What local development environment and container workflow should be adopted?
- Which evaluation, logging, and privacy controls are appropriate for each experiment?
- What hosting target, if any, should eventually be explored?

Resolve these when they become relevant; do not invent answers in advance.
