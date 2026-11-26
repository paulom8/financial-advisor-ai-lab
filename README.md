# Financial Advisor AI Lab

An educational prototype for learning AI capabilities and how they are used in real applications. The financial-advisor scenario provides synthetic examples; this is not a production financial-advice service.

## Project documents

- [Project charter](docs/project-charter.md): objectives, scope, and boundaries.
- [Architecture](docs/architecture.md): confirmed stack direction, current implementation, proposals, and open decisions.
- [Learning roadmap](docs/learning-roadmap.md): all 15 industry-prioritized AI and supporting technology categories, with progress tracking.
- [Progress log](docs/progress-log.md): completed milestones, current focus, and remaining learning areas.
- [Development principles](docs/development-principles.md): incremental learning and project practices.
- [Lessons learned](docs/lessons-learned.md): practical notes from learning with AI and coding agents.
- [Codex instructions](AGENTS.md): persistent instructions for coding agents working in this repository.

## Current status

The original React question page sends one synthetic question to `POST /api/ask`. FastAPI calls the OpenAI Responses API and may execute one validated, read-only function to retrieve PostgreSQL `Test` records; React displays the answer and whether the function was used. Each question starts a fresh request. A separate `GET /api/test-records` endpoint reads the same table. A separate document RAG page retrieves up to three plain-text sections and optionally sends only those sources to OpenAI. See the [architecture](docs/architecture.md) and [learning roadmap](docs/learning-roadmap.md).

## Learning pages

| Page | Experiment | What to try |
|---|---|---|
| [Ask the model](http://localhost:5173/) | Single question and answer | Ask “Explain compound interest.” Look for **Database function not used**. |
| [Ask the model](http://localhost:5173/) | Function calling with PostgreSQL | Ask “Which demo client has the largest savings target?” Look for **Database function used**. |
| [Evaluate the model](http://localhost:5173/evaluation) | Repeatable model evaluation | Run three preset questions. Compare expected and actual answers and see which questions used the database. Edit a fictional target to try a different expected winner. |
| [Ask the documents](http://localhost:5173/documents) | Keyword-based RAG | Retrieve passages without a model call, then ask the documents. Compare citations and answers; try a fee question to see missing evidence. |
| [Ask the documents](http://localhost:5173/documents) | Embeddings and semantic similarity | Enter "How big is your team?" and select **Compare keyword and semantic search**. Look for the Employees passage in the ranked results. The comparison uses OpenAI embeddings. |
| [FastAPI interactive docs](http://localhost:8000/docs) | PostgreSQL read through FastAPI | Run `GET /api/test-records` to see the saved fictional records directly. |

## Run locally

Use Python 3.11 or newer for the current FastAPI release, Node.js with npm (Vite requires `^20.19.0 || >=22.12.0`), and PostgreSQL. The backend initializes its sample table at startup, so the `financial_advisor_lab` database must already exist and be owned by the `financial_advisor_app` login.

**First-time setup.** Create `backend/.env` from [the example](backend/.env.example) only if the local file is missing. Set `DB_PASSWORD` and `OPENAI_API_KEY` in that ignored file. `OPENAI_MODEL` is optional and defaults to `gpt-6.2-sol`. Run the setup commands from the project root.

```powershell
python -m venv backend/.venv
.\backend\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
npm.cmd --prefix frontend ci
```

**Insert the fictional function-calling examples.** This explicit, repeatable command adds missing fictional clients and goals and preserves any amounts you edited. It runs separately from application startup. From the project root after configuring `backend/.env`:

```powershell
Push-Location backend
.\.venv\Scripts\python.exe -m app.seed_test_records
Pop-Location
```

To try a change in PostgreSQL, edit only the amount after `AUD $` on one of the five demo descriptions, using a value such as `85,000` or `85000`. The next database lookup reads the new value.

**Daily startup on Windows.** Open two terminals in the project root and keep both running. In the first terminal, start FastAPI and wait for `Application startup complete`.

```powershell
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --reload-dir backend/app --port 8000
```

In the second terminal, start Vite.

```powershell
npm.cmd --prefix frontend run dev
```

Open [the question page](http://localhost:5173). Submitting a question sends it to OpenAI and may incur API charges. Use synthetic, non-sensitive examples only.

## Troubleshooting

- **Connection refused.** Open [the local API docs](http://localhost:8000/docs). If they fail to load, check the FastAPI terminal for a startup error. If they load, compare the failed request URL with `http://localhost:8000/api/ask`. A frontend `VITE_API_URL` setting overrides the default backend address. Restart Vite after correcting it.
- **Key rejected after editing the local file.** Restart FastAPI after saving `backend/.env`. An `OPENAI_API_KEY` already set in the terminal that launches FastAPI takes precedence over the file. Keep the key in the backend environment only.

## Offline checks

From `backend`, run the question API regression tests. They exercise the FastAPI route and OpenAI SDK using a simulated provider. The suite runs without credentials or a database connection.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

From `frontend`, run the browser request helper tests and build the production bundle.

```powershell
npm.cmd test
npm.cmd run build
```
