# Lessons learned from developing with AI and Codex

## 1. Understand Git before you start

You need to understand repositories, branches, commits, merging, pushing, pulling, and rollback.

Otherwise, you risk overwriting working code, losing previous implementations, or not knowing which version is correct.

A repository holds your project and its history. A commit saves a point in that history. A branch gives you a place to work on a change. Learn how to merge branches, push your changes to a shared repository, pull other changes, and undo a change safely.

**Example.** Before trying a new design, commit the working version and do the redesign on a separate branch. If the redesign causes problems, you can get back to a version that worked.

## 2. Define the project before asking AI to build it

Before asking AI to build anything, understand the purpose of the application. Write down who will use it, what it should do, which screens users will see, how they will move between screens, and what business rules the app must follow. Describe the user workflows step by step.

Without a clear specification, AI may produce technically functional software that doesn't solve the intended problem.

**Example.** A demo advisor opens a fictional client record, enters a savings goal, and sees it on the client summary screen. The goal must be greater than zero.

## 3. Define the architecture before implementation

Decide how the frontend, backend, APIs, database, authentication, and external services will communicate and work together. The frontend is what users see, and the backend handles work behind the scenes. Authentication checks who is signing in. An API defines how one part asks another for data or an action.

Give each part a clear responsibility. When parts depend too heavily on each other, changing one can make the others harder to maintain.

**Example.** In the Financial Advisor AI Lab, React shows the screen, FastAPI handles requests, PostgreSQL stores records, and the AI model answers questions.

## 4. Break development into small, verifiable tasks

Asking Codex to build the entire application in one enormous prompt makes the result hard to review. Establish the overall specification first, then ask Codex to implement one logically independent feature at a time. Choose a piece you can review and test on its own. Small changes are easier to debug and undo.

**Example.** First ask Codex to show a list of fictional clients. Add a search box in a later task.

## 5. Never assume AI-generated code is correct

AI can produce code that looks excellent but contains logical errors, security vulnerabilities, missing validations, or incorrect business rules.

Every meaningful change should be tested against expected behaviour.

After Codex implements code, test that it behaves as expected before assuming the implementation is correct. Check the important actions and outcomes, including any data that should be saved or updated.

**Example.** After changing a fictional savings goal, reload the page and make sure the new amount is still there.

## 6. Make sure existing features still work

Before a big change, save the working version in a commit and make sure its tests pass. After adding something new, check that the old features still work. This is called regression testing.

**Example.** After adding search to a list, check that the full list comes back when you clear the search box.

## 7. Understand what Codex is changing

You don't necessarily need to understand every line of generated code, but you should understand the purpose and consequences of significant changes.

Review which files were modified, why they were modified, and whether the changes were within the requested scope. You know what you asked for, so review the result and decide whether it meets your needs. Codex can misunderstand even a simple request.

**Example.** If you asked Codex to change a button label and it also changed how the app saves records, ask why before accepting the work.

## 8. Keep development separate from the live app

Separate development and production. Use a development environment to try changes and a production environment for real users. Give each its own settings and keep passwords and API keys private. Decide how changes will be deployed and review AI's work before it goes live.

**Example.** Try a new feature locally with a test database. Put it in the live app after review.

## 9. Keep project notes up to date

As the project evolves, update the requirements, architecture decisions, API contracts, and development instructions. These notes explain what the app should do, how it is built, how its APIs work, and how people should work on it. If Codex reads outdated instructions, it may bring back a problem you've already fixed.

**Example.** Use separate Markdown files for project rules, how to work on the project, how the app is built, and what you have learned or finished. If a task moves from planned to done, update the progress notes.

## 10. Find out what went wrong before asking AI to fix it

Read the error, check the logs and any test results, and look at recent changes. Give Codex what you found so it can help trace the cause. Asking it to fix the same problem repeatedly can lead to more bugs.

**Example.** If a page shows “Connection refused,” check whether the server is running and which address the page is trying to reach. Share those details with Codex.

## 11. Define clear acceptance criteria

For every feature, specify what successful behaviour looks like. Write down what should happen in common cases and when something goes wrong. These checks are called acceptance criteria. They give Codex something concrete to implement and verify, and give you a way to review its work.

**Example.** For a document upload, say who can upload, which file types to support, how large a file can be, how to check that the file is valid, where it should be stored, and what message appears when it is rejected.

## 12. Protect data and control who can access it

Know how the app checks who is signed in (authentication), what each person is allowed to do (authorisation), and who can access the database. Protect sensitive data and API keys. Record important actions so you can review them later. This is called audit logging. An app can work as expected and still expose data.

**Example.** Use fictional client records when learning. In an app with real accounts, check that one user cannot open another user's record.

## 13. Use ChatGPT to think things through and Codex to work on the project

Use ChatGPT to explore ideas, ask questions, compare options, and spot missing requirements. It can turn a rough idea into a clear prompt for Codex. This helps you catch missing details early and avoid rework. Review the prompt and the decisions it contains before giving it to Codex.

Use Codex to inspect the project, organise files, or change code. With the right permissions, it can also run Windows commands and install programs or libraries. Understand what those actions will change before approving them.

Tell Codex what to build, which existing behaviour to preserve, what to inspect first, and how you will check the result.

**Example.** Ask ChatGPT to help draft a prompt such as “Read the existing client page. Add a search box that filters by name. Keep the save behaviour the same. Show me how to check that clearing the search brings back all clients.” Review the prompt, then give it to Codex.

## 14. Give related files a clear home

Architecture explains how the parts work together. The folder structure tells you where to find each part when something needs to change. Group files by their job and add folders as you need them. If you ask AI to suggest a layout, have it explain where things go and confirm that the layout fits the project before building on it.

**Example.** Keep screen code in `frontend/`, server code in `backend/`, and project notes in `docs/`. Give images and scripts a clear place when the project needs them. Keep database connection code together so it is easy to find.

## 15. Use semantic search to find information with different wording

Imagine a fictional company document says, “The company employs 42 people.” You ask, “How big is the team?” A search for the word “team” could miss that sentence. Semantic search can find it because both phrases are about the number of people who work there.

An embedding is a list of numbers that helps the computer compare the meaning of a question with the meaning of passages in files or a database. The AI can use the passage it finds to answer “42 employees.” Check the passage to see whether it supports the answer. If the source never gives a headcount, the answer is still unknown.

## The bigger lesson

1. **Plan.** Write down who will use the app, what they will do, and how you will know it works.
2. **Design.** Decide how the parts will fit together, where the data will go, and who can access it.
3. **Implement.** Build one small part at a time with Codex and use Git to save your progress.
4. **Verify.** Review the changes, try the new feature, and check that existing features still work.
5. **Release.** Put the change into use, watch for problems, and know how to go back to a working version.

Plan enough to make the next decision safely, then adjust as you learn.

## The principle I keep coming back to

Use AI to explore options and make decisions faster. Keep important decisions in your hands and learn enough to notice when the project is heading in the wrong direction. In this lab, ChatGPT can help you think through a decision, Codex can build a small change, and Git and testing help you review the result.

Producing code faster is one part of the work. Review and testing help you turn that code into software you can rely on.
