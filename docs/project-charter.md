# Project charter

## Purpose

Build a simple financial-advisor simulation as a practical laboratory for learning AI technologies, tools, and capabilities that are valuable across the software industry. The application provides a coherent setting for experiments; project fit does not override the learning priorities in the roadmap.

## Objectives

- Learn all 15 categories in [the learning roadmap](learning-roadmap.md), one small concept or experiment at a time.
- Build toward an advisor workflow that can capture synthetic client information, handle documents, interact with AI, identify missing information and possible contradictions, ask follow-up questions, and eventually produce a draft plan for human review.
- Develop transferable skills in AI application development and general software engineering.
- Use experiments that can be run, inspected, and discussed before moving to the next concept.

## Confirmed boundaries and requirements

- This is an educational prototype, not a production financial advice service.
- Use synthetic client data only. Do not enter real personal or financial client information.
- The application should remain simple, likely one or two screens; complexity belongs in purposeful learning experiments rather than unnecessary product surface.
- Learning all 15 categories is a must, but their order can be adjusted when a specific dependency or application step makes a detour useful. Follow the detour policy in the roadmap.
- Do not implement, install dependencies, or modify the repository without user approval.
- For now, use `main` as the integration branch and temporary feature branches for individual tasks. Push feature branches and use pull requests to review and merge into `main`. A separate `development` branch is not needed for the current learning project; revisit it if a distinct integration or staging workflow becomes useful.

## Scope

The eventual laboratory may explore model interaction, prompts, assistants, tools, RAG, documents and multimodal input, APIs and MCP, workflows, data, evaluation, security, coding agents, reusable components, architecture, and deployment. The detailed categories and priorities live in the roadmap.

## Non-goals

- Providing production financial advice or making unsupervised financial decisions.
- Using real client data.
- Building all planned capabilities up front.
- Adopting a technology solely because it is new, prominent in media, or convenient to the application.

## Status

**Confirmed:** purpose, educational nature, synthetic-data boundary, incremental learning, coverage of all 15 categories, flexible sequencing with explained detours, and the current `main` plus temporary feature-branch workflow.

**Proposed:** the detailed application structure and implementation sequence in [architecture](architecture.md) and [learning roadmap](learning-roadmap.md).
