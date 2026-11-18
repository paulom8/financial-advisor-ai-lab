# Instructions for Codex

Before project work, read [README.md](README.md) and the relevant documents under [docs/](docs/). Read all four project documents before proposing or changing architecture or roadmap decisions.

## Working rules

- This is an educational prototype using synthetic client data, not a production financial-advice service.
- Work incrementally: propose or implement one small concept/feature at a time, explain its purpose, and give the user room to inspect and learn before moving on.
- Do not treat recommendations or unresolved questions in project documents as approved decisions. Preserve the explicit status labels.
- Do not introduce technology just to increase complexity. Explain dependencies and practical value.
- The learning baseline is prioritised by real-world relevance, industry adoption, practical usefulness, and career value. Before any detour, explain why it supports a dependency, avoids rework, or improves the application's flow. After the detour, return to the baseline unless the user approves a change.
- Track category and experiment status in `docs/learning-roadmap.md`; use Not started, In progress, Explored, Completed, or Postponed, with a short note for postponements and detours.
- Never use real personal or financial client data in examples or experiments.
- Do not implement financial recommendations as authoritative advice. Keep generated content reviewable by a human.
- Do not install dependencies, implement features, or make repository changes without clear user authorization. Follow any more specific current user instruction.
- Do not run tests unless the user asks for testing or verification.

## Documentation maintenance

When the user approves a change to objectives, scope, architecture, dependencies, development practices, or roadmap priority, update the relevant source-of-truth document in the same task. Keep `README.md` concise and links current. Update this file only when the persistent agent workflow changes. Clearly identify confirmed decisions, proposals, and open questions; do not silently convert one into another.
