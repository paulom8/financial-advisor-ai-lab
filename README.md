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

The first slice is a small React page backed by a Python FastAPI API and PostgreSQL. It lists records from the `Test` table; the API initializes the table and inserts one synthetic sample row when the table is empty. This is a supporting application foundation, not the end goal. See [architecture](docs/architecture.md) and [learning roadmap](docs/learning-roadmap.md).

## Run locally

The setup commands are for the first run or a new checkout. Once dependencies are installed, skip the setup commands and use only the start commands.

1. Ensure PostgreSQL is running with the `financial_advisor_lab` database and `financial_advisor_app` login. Copy `backend/.env.example` to `backend/.env` if needed, then set `DB_PASSWORD` there.
2. In a terminal, from `backend/`, create the virtual environment and install backend dependencies once, then start the API:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

3. In a second terminal, from `frontend/`, install frontend packages once, then start the page:

   ```powershell
   npm install
   npm run dev
   ```

Use synthetic data only.
