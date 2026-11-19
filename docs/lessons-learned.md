# Lessons learned from developing with AI and Codex

1. Understand Git and version control before developing

You need to understand repositories, branches, commits, merging, pushing, pulling, and rollback.

Otherwise, you risk overwriting working code, losing previous implementations, or not knowing which version is correct.

2. Define the project before asking AI to build it

You need to understand the purpose of the application, its navigation, screens, functionality, business rules, and user workflows.

Without a clear specification, AI may produce technically functional software that doesn't solve the intended problem.

3. Define the architecture before implementation

Decide how the frontend, backend, APIs, database, authentication, and external services will communicate.

For example, in your Financial Advisor AI Laboratory, React, FastAPI, PostgreSQL, and LLM integrations should have clearly defined responsibilities.

Otherwise, AI might produce tightly coupled code that becomes difficult to maintain.

4. Break development into small, verifiable tasks

Don't ask Codex to build the entire application in one enormous prompt.

Instead, establish the overall specification, then implement one logically independent feature at a time.

This makes reviewing, testing, debugging, and reverting changes much easier.

5. Never assume AI-generated code is correct

AI can produce code that looks excellent but contains logical errors, security vulnerabilities, missing validations, or incorrect business rules.

Every meaningful change should be tested against expected behaviour.

After Codex implements code, test that it behaves as expected before assuming the implementation is correct. Check the important actions and outcomes, including any data that should be saved or updated.

6. Protect working functionality

Before significant changes, ensure the current version is committed and tests pass.

After implementing new functionality, verify that existing functionality still works. This is called regression testing.

7. Understand what Codex is changing

You don't necessarily need to understand every line of generated code, but you should understand the purpose and consequences of significant changes.

Review which files were modified, why they were modified, and whether the changes were within the requested scope. In the end, you are the one who knows exactly what needs to be done, so review the result and decide whether it is right. Don't expect AI to perform every task correctly.

8. Establish development environments

Separate development and production. Use appropriate configuration, secrets management, and deployment procedures.

AI should not be making unreviewed changes directly to a live production environment.

9. Keep specifications and documentation updated

As the project evolves, update the requirements, architecture decisions, API contracts, and development instructions.

Otherwise, Codex may work from outdated assumptions and reintroduce previously corrected problems.

Keep project documentation organised by purpose. Separate Markdown files can cover working flow, project rules, architecture, roadmap and progress, or other important topics. This makes each source of information easier to find and update without mixing unrelated instructions.

10. Learn to diagnose problems instead of blindly prompting AI

When something doesn't work, investigate the logs, errors, tests, and recent changes.

Repeatedly telling AI to "fix it" without understanding the problem can introduce further bugs.

11. Define clear acceptance criteria

For every feature, specify what successful behaviour looks like.

For example, instead of "Create a document upload feature", specify supported formats, file-size limits, validation, storage behaviour, error handling, and permissions.

This gives Codex something concrete to implement and verify.

12. Understand security and data protection

Especially for a financial application, you need to understand authentication, authorisation, sensitive data, API keys, database access, and audit logging.

Functional software is not necessarily secure software.

13. Use ChatGPT and Codex for different, complementary purposes

Use Codex mainly for hands-on work in the project: understanding and organizing its structure, writing or changing code, and supporting development.

Codex can also interact with the development environment. Depending on the available permissions and tools, it can run Windows or terminal commands and install programs or project dependencies. Understand what commands and installations will do, and review them because they may change the computer or project.

Use ChatGPT for broader support around the project, such as exploring ideas, asking general questions, thinking through requirements and trade-offs, or preparing a clear prompt for Codex. These conversations can support the project without requiring ChatGPT to make the code changes itself.

Instead of sending rough ideas directly to Codex, use ChatGPT to discuss the requirements, evaluate approaches, identify missing details, and produce a well-structured implementation prompt. Once it accurately represents your intentions, review it and give it to Codex.

Benefits:
- Reduces misunderstandings and ambiguity.
- Prevents important requirements from being forgotten.
- Helps identify missing information before implementation.
- Makes Codex's tasks more focused and precise.
- Reduces unnecessary code changes and rework.

A good Codex prompt should specify not only what to implement, but also what must not change, how success will be verified, and whether Codex should inspect the existing code before making changes.

ChatGPT can help produce a clearer prompt, but that doesn't guarantee the requirements or technical decisions are correct. They still need to be reviewed.

14. Plan how the software and its files will be structured

Architecture describes how parts of the application communicate. The codebase also needs a clear structure so related files are easy to find and maintain.

For example, keep the frontend and backend in clearly separated areas, and group documentation, images, scripts, and database-related code where they belong. Choose folders that fit the project rather than adding folders without a purpose.

If you are unsure how to organise the project, ask AI to propose a structure and explain where each part belongs. Review the proposal against the project's needs, and confirm the structure before asking AI to build on it. AI can help create the structure, but it cannot guarantee that its first proposal is the right one.

The bigger lesson

I would summarise everything in five stages:
1. Plan
   Requirements, workflows, navigation, acceptance criteria
2. Design
   Architecture, data model, APIs, security
3. Implement
   Codex, small tasks, Git, commits
4. Verify
   Code review, tests, regression checks
5. Release
   Deployment, monitoring, recovery

One distinction matters: you don't need to finish designing every detail before writing code. You need enough understanding to make the next implementation decision safely, while allowing controlled changes as you learn.

One additional principle I'd put above everything else

AI should accelerate your decisions, not make important decisions without your understanding.

For your Financial Advisor AI Laboratory, that means using ChatGPT to evaluate requirements, architecture, trade-offs and implementation approaches; then using Codex to implement well-defined tasks, with Git and tests protecting the results.

The goal isn't to become an expert in every technology before starting. It's to understand enough to recognise when AI is taking your project in the wrong direction.

And perhaps the most important practical lesson: producing code faster is not the same as producing reliable software faster.
