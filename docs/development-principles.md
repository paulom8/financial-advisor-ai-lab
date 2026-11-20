# Development principles

## Learning workflow

- Build and study one small concept or feature at a time. State what it does, why it matters, what is application code versus a provider/development-tool capability, and what the experiment should demonstrate.
- Keep the app simple. Use the financial-advisor scenario as a coherent source of synthetic examples, not as the reason to prioritise a technology over industry value.
- After each experiment, explain the result and update the [roadmap tracker](learning-roadmap.md) accurately before proposing the next step.
- Explain and record any temporary roadmap detour, then return to the baseline after it is complete.
- Do not silently treat a suggestion, generated plan, or implementation detail as an approved decision.

## Safety and quality

- Use synthetic client information only. Never put real financial or personal client information into prompts, documents, test fixtures, logs, or screenshots.
- Keep model-produced findings clearly distinguishable from verified facts. Contradictions and follow-up questions are suggestions for advisor review.
- Human review is required for any eventual draft financial plan. The prototype must not present itself as providing production financial advice.
- Validate model outputs and tool arguments in application code. Model output is not authorization; tools should be narrow and explicitly allowlisted.
- Introduce tests and evaluation with the relevant feature. Do not claim quality from a few informal examples; use repeatable synthetic cases where practical.
- Keep secrets out of source control and avoid sending unnecessary data to external services.

## Git and development environment

**Current branch strategy:** use `main` as the integration branch and create a temporary feature branch for each task. Push the feature branch and review it through a pull request before merging to `main`. A separate `development` branch is not needed for the current learning project; revisit it if a distinct integration or staging workflow becomes useful. Show the exact Git command whenever one is run or suggested, and briefly explain its effect so the user can learn Git through the work.

Local development uses a Python virtual environment and pip for the backend, npm and Vite for the frontend, and a local PostgreSQL database. The [README](../README.md#run-locally) contains the startup commands. Docker and cloud hosting remain future learning topics.

## Codex collaboration and documentation

- Read persistent project instructions and relevant source-of-truth documents before work.
- Before a substantial implementation, describe the small scope and the learning goal. Work only within the user's authorization; do not install packages or expand scope without approval.
- Report changes, rationale, and verification honestly. Do not run tests unless asked to test or verify.
- When the user approves a change to project objectives, scope, architecture, dependencies, development practices, or roadmap priorities, update the relevant document in the same task. Keep confirmed decisions, recommendations, and unresolved questions clearly separated.
- Keep `AGENTS.md` concise and operational; place detailed project knowledge in the appropriate `docs/` file.
