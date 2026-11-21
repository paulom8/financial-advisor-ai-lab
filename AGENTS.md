# Instructions for Codex

Before project work, read [README.md](README.md) and the relevant documents under [docs/](docs/). Read all four core project documents before proposing or changing architecture or roadmap decisions.

## Working rules

- This is an educational prototype for learning AI capabilities and how they are used in real applications, not a production financial-advice service.
- Work incrementally: propose or implement one small AI concept or feature at a time. Explain its purpose and what it should help the user learn, then give the user room to inspect and learn before moving on.
- Preserve existing pages, features, and ways to try earlier experiments when adding a new capability. Get explicit user approval before replacing or removing any of them. Update the [learning pages index](README.md#learning-pages) when pages or their experiments change.
- The learning baseline is prioritized by real-world relevance, industry adoption, practical usefulness, and career value—not by which topic is easiest. Before a detour, explain how it supports a dependency, avoids rework, or improves the application's flow. After the detour, return to the baseline unless the user approves a change.
- Do not treat recommendations or unresolved questions in project documents as approved decisions. Preserve explicit status labels.
- Keep the page understandable and the software purposeful. The user already knows programming; do not turn the work into programming lessons, but do implement supporting software when it enables a worthwhile AI experiment.
- Track category and experiment status in `docs/learning-roadmap.md`; use Not started, In progress, Explored, Completed, or Postponed, with a short note for postponements and detours.
- Use synthetic data only. Never use real personal or financial client data in examples or experiments.
- Do not present generated financial content as authoritative advice. Keep it reviewable by a human.
- Check existing tools and dependencies before installing anything. Do not install dependencies, implement features, or make repository changes without clear user authorization. Follow any more specific current user instruction.
- Do not run tests unless the user asks for testing or verification. When verification is requested, state acceptance criteria first and ask before running if the user asks for approval.
- When an error is reported, trace the actual code and runtime path. Use the available evidence to diagnose paths, missing components, configuration, network boundaries, and logic. Respect the user's verification instructions.
- When using Git, show each exact command run or suggested and briefly explain what it did or will do.
- Leave changes available locally for the user to review after testing. Commit, push, or merge only when the user explicitly authorizes that action.

## Documentation maintenance

When the user approves a change to objectives, scope, architecture, dependencies, development practices, or roadmap priority, update the relevant source-of-truth document in the same task. Keep `README.md` concise and links current. Update this file only when persistent agent workflow changes. Clearly identify confirmed decisions, proposals, and open questions; do not silently convert one into another.
