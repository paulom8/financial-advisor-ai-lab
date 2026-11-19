# Learning roadmap

## Prioritisation principle

The baseline order reflects a practical synthesis of broad industry use, transferable usefulness, durability, and likely career value. There is no authoritative universal ranking of these exact categories, and importance varies by job role. Industry evidence informs the ranking but does not make it a job-posting count. Examples include the [Stack Overflow Developer Survey](https://survey.stackoverflow.co/2026), [GitHub Octoverse](https://github.blog/news-insights/octoverse/octoverse-2025/), [Google DORA 2025 research](https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/), and [CNCF's 2025 cloud-native survey](https://www.cncf.io/reports/the-cncf-annual-cloud-native-survey/). Survey audiences and methods differ; interpret adoption figures in that context.

The rank is a **priority baseline, not a mandatory implementation sequence**. Establish durable software foundations while learning AI-specific capabilities. Do not mistake media attention or novelty for practical value.

## Industry-prioritised categories

| Rank | Category | Why it matters / status |
|---:|---|---|
| 1 | **10. Data processing and databases** | Core to nearly all applications; highly transferable. Established foundation. |
| 2 | **13. AI development tools and coding agents** | AI-assisted coding is increasingly part of software work; review, debugging, and verification remain essential. Adopted and changing quickly. |
| 3 | **15. AI application architecture and deployment** | Connects application components and makes software operable. Containers/cloud are broadly useful; orchestration depth is role-dependent. Established, with varying depth by role. |
| 4 | **8. APIs, SDKs, MCP, connectors, plugins and integrations** | API/SDK integration is common software work; MCP and similar AI protocols are newer. Learn integration fundamentals first. Mixed: established APIs, emerging protocols. |
| 5 | **11. AI evaluation, testing and observability** | AI behavior varies; evaluation and operational visibility help make features dependable. Important and maturing. |
| 6 | **12. Security, privacy and governance** | Durable software responsibilities, with additional data and tool risks in AI applications. Established discipline; AI-specific practice evolving. |
| 7 | **5. Tools and function calling** | Lets models request application actions or information; the application must validate and execute safely. Common AI application pattern. |
| 8 | **1. AI interaction and model capabilities** | Text, streaming, structured responses, reasoning modes, and multimodal input are model interfaces. Core capabilities evolve rapidly; not all are needed in every app. |
| 9 | **2. Prompt engineering and instructions** | Instructions and examples shape output. Useful, but strongest when combined with engineering, evaluation, and context design. Core practice, not a standalone architecture. |
| 10 | **9. Automation and workflows** | Connects steps, systems, and people; AI autonomy should be bounded and justified. Established workflows; AI automation evolving. |
| 11 | **6. Knowledge management, context and RAG** | Useful for grounding answers in a corpus, but adds ingestion, retrieval, and evaluation complexity. Valuable in knowledge-heavy applications; not universal. |
| 12 | **7. Documents and multimodal AI** | Enables document/image/audio use cases, with added extraction, source, and privacy concerns. Useful, with uneven adoption by modality. |
| 13 | **3. AI assistants and customisation** | Reusable instructions, context, and memory patterns are useful; vendor-specific assistant abstractions change. Concepts common, features vary. |
| 14 | **14. Reusable AI components, skills and templates** | Reuse helps after behavior and boundaries are understood; specific formats can be tool-dependent. Useful practice, narrower direct demand. |
| 15 | **4. AI agents and multi-agent architecture** | Can help multi-step tool workflows but add coordination, cost, latency, and failure modes. Emerging and task-dependent; not a default design. |

## Flexible sequencing policy

1. Use the ranking above as the default basis for learning priority.
2. A topic may move earlier when a concrete feature has a dependency on it, a detour improves the application's development flow, or learning it now avoids meaningful rework.
3. Before changing sequence, explain the reason, expected learning outcome, affected roadmap items, and whether the change is temporary.
4. Keep the detour small. Do not add technology only to make the application more complex.
5. After completing the feature or experiment, return to the baseline unless the user approves a revised priority.
6. Record detours, postponements, and their rationale in the progress log below.

## Suggested experiment order (flexible, not yet approved as a fixed build plan)

The following is a learning-friendly starting sequence, not an approved commitment to implement all steps in this exact order:

1. Show static text in a minimal React screen.
2. Add a minimal FastAPI endpoint and display its response.
3. Replace or augment that response with one model API call.
4. Change a prompt/instruction and compare outputs on the same synthetic input.
5. Add deterministic missing-field validation and present possible AI-identified contradictions/questions.
6. Add structured output, validation, and focused evaluation examples.
7. Persist synthetic client/conversation data in PostgreSQL when persistence is useful.
8. Add a narrow, safe tool call; then introduce workflow orchestration.
9. Add a second provider only when comparison is useful; measure latency, usage/cost, errors, and task-specific quality before considering fallback/routing.
10. Add document extraction, then retrieval/RAG with source references.
11. Explore assistant configurations, reusable components, and an integration/MCP experiment.
12. Explore bounded agent workflows and multimodal/voice capabilities where useful.
13. Expand security, testing, observability, CI/CD, Docker, and deployment as the application grows.

Several experiments can be moved earlier or split into smaller lessons. The user should be able to inspect and understand one concept before moving on.

## Progress tracker

Status definitions: **Not started** = no experiment; **In progress** = current experiment; **Explored** = tried and discussed; **Completed** = experiment works and was reviewed; **Postponed** = intentionally deferred with a reason. Update this tracker as work is approved and completed. Do not imply completion from a discussion alone.

| Rank | Category | Status | Notes / detour or postponement reason |
|---:|---|---|---|
| 1 | Data processing and databases | Explored | PostgreSQL `Test` table was initialized, one synthetic record was seeded, and the React page displayed it. |
| 2 | AI development tools and coding agents | Not started | |
| 3 | AI application architecture and deployment | Not started | |
| 4 | APIs, SDKs, MCP, connectors, plugins and integrations | Explored | Temporary API detour served PostgreSQL rows to the requested React page; return to the priority baseline after this slice review. |
| 5 | AI evaluation, testing and observability | Not started | |
| 6 | Security, privacy and governance | Not started | |
| 7 | Tools and function calling | Not started | |
| 8 | AI interaction and model capabilities | Not started | |
| 9 | Prompt engineering and instructions | Not started | |
| 10 | Automation and workflows | Not started | |
| 11 | Knowledge management, context and RAG | Not started | |
| 12 | Documents and multimodal AI | Not started | |
| 13 | AI assistants and customisation | Not started | |
| 14 | Reusable AI components, skills and templates | Not started | |
| 15 | AI agents and multi-agent architecture | Not started | |
