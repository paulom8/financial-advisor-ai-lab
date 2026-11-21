# Development principles

## Learning workflow

- Work incrementally: propose or implement one small AI concept or feature at a time. Explain its purpose, what the learner should notice, and which capability or industry pattern it teaches.
- Give the user room to inspect and learn before moving on to another concept.
- Keep every existing feature and learning page available when adding an experiment. Experiments can share a page when each remains easy to try. Maintain the [learning pages index](../README.md#learning-pages) with the location and learning purpose of each page. Ask the user before replacing or removing an existing feature or page.
- Distinguish the AI/provider capability from the application code or development tool used to expose it.
- Use the industry-prioritized roadmap as the baseline. The baseline reflects real-world relevance, industry adoption, practical usefulness, and career value—not ease or implementation effort.
- Before a detour, explain how it supports a dependency, avoids rework, or improves the application's learning flow; describe the expected learning outcome and affected roadmap items. Return to the baseline after a temporary detour unless the user approves a change.
- After an experiment, explain what happened and update the [roadmap tracker](learning-roadmap.md) accurately.
- Keep suggestions, proposals, confirmed decisions, and open questions distinct.

## AI experiments and software

- The user already knows programming. Do not turn the project into programming lessons; explain implementation detail only when it helps answer an AI learning question or the user asks.
- Keep the application experience clear and focused on exploring AI. Use the React page, a provider interface, or both depending on what best demonstrates the concept.
- Do not avoid an industry-relevant AI concept just because it needs an API, SDK, connector, database, or other supporting capability. Explain the role of that dependency and check whether it already exists before installing anything.
- Avoid adding technology only for complexity. Prefer purposeful integrations and explain their practical value.
- Do not install dependencies or change the repository without clear user authorization. Follow any more specific current instruction.

## Safety and quality

- Use synthetic client information only. Never put real personal or financial client data into prompts, documents, test fixtures, logs, or screenshots.
- This is an educational prototype, not a production financial-advice service. AI-generated findings and draft plans are suggestions for human review, not authoritative advice.
- Keep AI outputs distinguishable from verified facts. Discuss uncertainty, source support, and limitations.
- Validate model outputs and tool arguments where application behavior depends on them. A model request does not authorize an action; keep tools bounded and explicit.
- Use repeatable synthetic examples when comparing behavior. Do not claim broad quality from a few informal trials.
- Keep secrets out of source control and avoid sending unnecessary data to external services.

## Git and development environment

**Current branch strategy:** use `main` as the integration branch and a temporary feature branch for each task. Push feature branches and review them through pull requests before merging to `main`. A separate `development` branch is not needed unless a distinct integration or staging workflow becomes useful. Show each exact Git command whenever one is run or suggested, and briefly explain its effect.

Local development uses a Python virtual environment and pip for the backend, npm and Vite for the frontend, and a local PostgreSQL database. The [README](../README.md#run-locally) contains the startup commands. Check existing tools and dependencies before proposing installations. Explore Docker and cloud hosting when they support an industry-relevant learning objective.

## Codex collaboration and documentation

- Read persistent project instructions and relevant source-of-truth documents before work.
- Before a substantial implementation, describe the small concept/feature and its learning purpose. Work only within user authorization.
- Do not run tests unless the user asks for testing or verification. Report changes and verification honestly.
- When the user approves a change to objectives, scope, architecture, dependencies, practices, or roadmap priorities, update the relevant document in the same task.
- Keep `AGENTS.md` concise and operational; document project learning decisions in the appropriate source-of-truth file.
