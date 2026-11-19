# Project charter

## Purpose

Build a simple financial-advisor simulation as a practical laboratory for learning AI capabilities and how AI is used in real applications. The app provides a coherent place to explore the technology; the learning priorities come from real-world relevance, industry adoption, practical usefulness, and career value.

The user already knows programming and does not want a programming curriculum. The application can include more capable software when it serves a worthwhile AI learning experiment, but complexity is not itself a goal.

## Objectives

- Learn all 15 categories in [the learning roadmap](learning-roadmap.md), one small concept or experiment at a time, with each topic tied to its practical role in AI applications.
- Explore what AI systems can do, how the capabilities are used in applications, where they work well, and where they fail.
- Develop practical understanding of models, prompts, multimodal input and output, tools, integrations, workflows, agents, evaluation, and responsible use.
- Use coding agents and other AI development tools as part of learning how AI is used in software work, while reviewing their output.
- Build toward an advisor workflow that can handle synthetic client information and documents, interact with AI, identify missing information or possible contradictions, ask follow-up questions, and eventually produce draft content for human review.
- Keep each experiment inspectable and discuss what it demonstrates before moving to another concept.

## Confirmed boundaries and requirements

- This is an educational prototype, not a production financial-advice service.
- Use synthetic client data only. Never enter real personal or financial client information.
- Work incrementally. State the learning purpose of each small concept or feature and allow time to inspect and learn before moving on.
- The roadmap priority baseline reflects industry relevance and usefulness, not topic difficulty or implementation convenience. Explain any detour in terms of dependency, avoided rework, or improved application flow.
- The app should provide a simple, coherent learning experience. Its implementation may grow when an AI experiment justifies it; do not add technology just for complexity.
- Do not present model output as authoritative financial advice. Keep generated content reviewable by a human.
- Use `main` as the integration branch and temporary feature branches for individual tasks. Push feature branches and use pull requests to review and merge to `main`. A separate `development` branch is not needed for the current project; revisit if a distinct integration or staging workflow becomes useful.

## Scope

The roadmap covers data and application foundations that are useful for AI systems, AI development tools and coding agents, application architecture, APIs/SDKs/MCP/connectors/plugins, evaluation, security and governance, model interaction, prompts, tools and function calling, context and RAG, documents and multimodal AI, assistants, workflows, reusable components, and agents. These areas support the wider goal of learning AI capabilities and applications.

## Non-goals

- Teaching programming or general software development as an end in itself.
- Providing production financial advice or making unsupervised financial decisions.
- Using real client data.
- Building every capability up front or introducing technology without a practical learning reason.

## Status

**Confirmed:** educational purpose; synthetic-data boundary; incremental, inspectable learning; industry relevance and practical usefulness as the priority basis; software as a means to explore AI; current `main` plus temporary feature-branch workflow.

**Proposed:** the detailed learning sequence in [the roadmap](learning-roadmap.md) and application structure in [architecture](architecture.md). Individual providers, models, and integrations remain open until a specific experiment needs them.
