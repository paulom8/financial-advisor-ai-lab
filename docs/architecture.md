# Architecture

This document distinguishes confirmed direction, current implementation, and proposals. The application is a learning environment for AI capabilities and their use in real applications. Keep architecture purposeful: use it to make an experiment work, not as a separate programming curriculum.

## Confirmed direction

- Frontend: React.
- Backend: Python FastAPI.
- Database: PostgreSQL.
- Version control: Git and GitHub.
- Use local development first. Docker and cloud hosting may be explored later when they support a learning objective.
- AI provider and model choice is open. OpenAI, Anthropic, and Google are possible providers to consider; these examples are not a mandate to use any specific provider or all three.
- The system may eventually support experiments comparing models or providers. Add comparison or fallback behavior only when a concrete learning question makes it useful.
- Use synthetic data only. Keep secrets on the backend when a provider API is connected.

## Current implementation

- React page built with Vite.
- FastAPI backend with SQLAlchemy.
- PostgreSQL database named `financial_advisor_lab`, using a dedicated `financial_advisor_app` login role and local ignored environment file for its password.
- The `Test` table has an incrementing integer `id`, a `description` up to 255 characters, and a `date_inserted` timestamp. Startup initializes the table and inserts a synthetic sample only when the table is empty.
- `GET /api/test-records` returns the table rows for display on the page.

This first slice established a working page/API/database path. It is a useful base for AI experiments, not an instruction to keep expanding database features.

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

A future AI experiment may connect the page through FastAPI to a model API or SDK, show model input and output, and allow comparison. Application logic should handle secrets, validate structured outputs, and control any tool execution. Add persistence only if saving synthetic experiments is useful. This is a proposed shape, not a requirement to build every component.

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
- Add document extraction before retrieval over documents; retain source references when AI answers rely on sources.
- Multi-agent workflows, deployment, and infrastructure expansion should have a clear learning reason. They are not required architecture milestones.

## Open questions

- Which capability should the next experiment explore?
- Which model/provider and access path best fit that capability and its industry use?
- Should the experiment run in this page, a provider interface, or both for comparison?
- Which API, SDK, connector, plugin, or MCP integration is relevant to the chosen experiment?

Resolve these questions as they become relevant; keep proposals distinct from confirmed decisions.
