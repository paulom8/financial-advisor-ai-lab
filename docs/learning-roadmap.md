# Learning roadmap

## Prioritisation principle

The baseline order reflects real-world relevance, industry adoption, practical usefulness, and likely career value. It is a reasoned synthesis, not a universal ranking or a job-posting count. Importance varies by role and industry. Examples of industry evidence include the [Stack Overflow Developer Survey](https://survey.stackoverflow.co/2026), [GitHub Octoverse](https://github.blog/news-insights/octoverse/octoverse-2025/), [Google DORA 2025 research](https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/), and [CNCF's 2025 cloud-native survey](https://www.cncf.io/reports/the-cncf-annual-cloud-native-survey/). Their audiences and methods differ, so interpret figures in context.

The ranking is **not based on which topics are easiest or quickest to implement**. Use it as a default learning priority, while keeping every category in scope. Some categories are AI capabilities; others are important tools and foundations for using AI in real applications. Software work supports the learning goal and is not a programming curriculum.

AI capabilities and industry practices change quickly. Treat this as a living map, not an exhaustive or permanent list; revisit it when widely used capabilities or integration patterns emerge.

## Industry-prioritised categories

| Rank | Category | Why it matters / status |
|---:|---|---|
| 1 | **10. Data processing and databases** | Applications need data to be collected, shaped, stored, and retrieved. Learn the AI-relevant role of data; do not expand database work without a learning reason. |
| 2 | **13. AI development tools and coding agents** | AI-assisted software work is increasingly common. Learn how agents inspect, change, and verify work, and how to review their results. |
| 3 | **15. AI application architecture and deployment** | AI features operate within real applications and services. Learn the main patterns and operational concerns at a useful level; infrastructure depth varies by role. |
| 4 | **8. APIs, SDKs, MCP, connectors, plugins and integrations** | APIs and SDKs are common ways to use model providers and connect services; MCP and related AI integration patterns are newer. Learn established integration basics and understand where newer approaches fit. |
| 5 | **11. AI evaluation, testing and observability** | AI outputs vary. Evaluation and operational visibility help teams understand quality, changes, failures, and usage. |
| 6 | **12. Security, privacy and governance** | Data protection and security remain core responsibilities, with added risks from models, prompts, and tools. |
| 7 | **5. Tools and function calling** | Models can request application actions or information. The application must validate requests and control execution. |
| 8 | **1. AI interaction and model capabilities** | Learn text, structured responses, streaming, reasoning modes, and multimodal input/output; available capabilities vary by model. |
| 9 | **2. Prompt engineering and instructions** | Instructions and examples shape model behavior. Learn by changing prompts and comparing results, alongside context and evaluation. |
| 10 | **9. Automation and workflows** | AI can participate in multi-step processes involving systems and people. Learn how to bound automation and retain appropriate human review. |
| 11 | **6. Knowledge management, context and RAG** | Retrieval can ground responses in a supplied corpus. It adds ingestion, retrieval, source handling, and evaluation work. |
| 12 | **7. Documents and multimodal AI** | Models can work with documents, images, audio, and other modalities; extraction errors and privacy concerns matter. |
| 13 | **3. AI assistants and customisation** | Reusable instructions, knowledge, and memory can shape an AI experience; provider-specific features change. |
| 14 | **14. Reusable AI components, skills and templates** | Reuse can make useful AI behavior repeatable once its purpose and boundaries are understood. |
| 15 | **4. AI agents and multi-agent architecture** | Agents can handle multi-step tasks, but coordination can add cost, delay, and failure modes. Learn them as a capability and use them where appropriate. |

## Flexible sequencing policy

1. Use the industry-prioritized ranking as the default basis for learning; do not reorder topics merely because one is easier to implement.
2. A topic may move earlier when a concrete AI feature depends on it, the detour avoids meaningful rework, or it improves the application's learning flow.
3. Before a detour, explain the reason, what the user will learn, which roadmap items are affected, and whether the change is temporary.
4. Keep the implementation as small as the learning question allows, without avoiding useful capability exploration just because it requires supporting software.
5. After a detour, return to the baseline unless the user approves a revised priority.
6. Record detours, postponements, and their rationale in the progress tracker.

## Suggested experiment order (flexible, not a fixed implementation plan)

1. Explore the current priority baseline one small concept at a time. Use AI development tools and coding agents to inspect or verify a focused behavior, then review what the agent did.
2. Learn how model APIs and SDKs connect AI capabilities to applications; compare provider options when it answers a useful question.
3. Explore model interaction, prompting, structured output, context, and multimodal capabilities through repeatable synthetic examples.
4. Study evaluation, safety, and privacy alongside the capabilities they affect.
5. Continue into tools/function calling, integrations (including MCP, connectors, and plugins), retrieval, assistants, and workflows.
6. Explore bounded agents and multi-agent patterns when the baseline leads there and the use case justifies them.

The app may use a provider playground, this page, or both. Choose the simplest practical interface for the learning question. The purpose is understanding AI capabilities and industry patterns, not accumulating code.

## Progress tracker

Status definitions: **Not started** = no experiment; **In progress** = current experiment; **Explored** = tried and discussed; **Completed** = experiment works and was reviewed; **Postponed** = intentionally deferred with a short note. Update status based on what was actually tried; do not imply completion from discussion alone.

| Rank | Category | Status | Notes / detour or postponement reason |
|---:|---|---|---|
| 1 | Data processing and databases | Explored | Existing PostgreSQL sample-record path is supporting application context. Five explicitly seeded fictional goals support the function-calling experiment. |
| 2 | AI development tools and coding agents | Explored | Used Codex for a focused endpoint verification; broader coding-agent capabilities remain to explore. |
| 3 | AI application architecture and deployment | Not started | |
| 4 | APIs, SDKs, MCP, connectors, plugins and integrations | Explored | Called OpenAI through its Python SDK behind a FastAPI route and displayed the response in React. MCP, connectors, and plugins remain to explore. |
| 5 | AI evaluation, testing and observability | In progress | Added regression tests for the question flow. The current experiment checks a live model's tool choice and answers on three preset questions. Broader observability remains open. |
| 6 | Security, privacy and governance | Not started | |
| 7 | Tools and function calling | Completed | Verified and reviewed the single read-only PostgreSQL function, approved fictional dataset, result limit, and React indicator. |
| 8 | AI interaction and model capabilities | Explored | Sent a synthetic question and reviewed the returned text in the React page. |
| 9 | Prompt engineering and instructions | Not started | |
| 10 | Automation and workflows | Not started | |
| 11 | Knowledge management, context and RAG | In progress | Temporary approved detour: keyword-based RAG and semantic retrieval completed and reviewed. Vector databases are next. |
| 12 | Documents and multimodal AI | Not started | |
| 13 | AI assistants and customisation | Not started | |
| 14 | Reusable AI components, skills and templates | Not started | |
| 15 | AI agents and multi-agent architecture | Not started | |

## Experiment log

- **Database round trip — Explored.** The first React page displayed a seeded PostgreSQL record. The temporary detour into HTTP APIs let the browser read the same data through FastAPI.
- **One question, one answer — Completed (20 November 2026).** The user saw a response in FastAPI's interactive docs, then confirmed the React page worked after correcting its API port and starting the backend. The walkthrough covered how a question reaches the model and how the answer returns to the page. This temporary detour combined API integration with model interaction so the user could inspect a real response. Future experiments follow the priority baseline.
- **Question-flow regression review — Completed (20 November 2026).** Offline checks cover the SDK request, provider errors, validation and malformed responses. A live browser submission returned the expected answer to a fictional arithmetic question, and the database endpoint returned its sample row.
- **Database function calling — Completed (22 November 2026).** Added a bounded `list_test_records` tool and an explicit seed command. The repeat seed added zero rows. Live examples confirmed that saved-record questions use the tool, absent clients are reported as absent from the result, and a general question answers directly. The React page displayed the database answer and badge. The final review restricted the tool to the approved fictional descriptions and verified the revised path with 11 backend tests, seven frontend tests, a production build, and live PostgreSQL and OpenAI checks. The user approved integration.
- **Model evaluation — In progress (22 November 2026).** Added a separate page to check the expected tool use and answer for three preset questions. The expected winner comes from a PostgreSQL snapshot, so editing a target can change the result on the next run. This experiment uses the existing tool flow and gives later model or instruction changes a baseline to compare.

- **Plain-text RAG - Completed (26 November 2026).** The user reviewed live Sunday and after-hours questions; both retrieved opening hours and main contact and generated correctly cited answers. The initial Saturday failure demonstrated a keyword matching limitation; weekend synonym normalization resolved the retrieval gap. Full backend integration verification remains environment-blocked.

### Approved RAG learning sequence (temporary detour)

1. Keyword-based RAG - Completed.
2. Embeddings and semantic similarity - Completed (26 November 2026). In live review, semantic search found Operating history for "How long has the company been in the market?"
3. Vector databases - In progress. Nine demo passage embeddings are saved. The search ranks the stored passages in PostgreSQL. Live review is pending.
4. Hybrid search - Not started.
5. Reranking - Not started.
6. RAG evaluation - In progress. Moved ahead of hybrid search and reranking to measure the current baseline first. Three cases compare keyword and saved-vector retrieval and answers. Live review is pending.
7. Advanced and conversational RAG - Not started.

Return to the industry-prioritised baseline after the approved detour.
