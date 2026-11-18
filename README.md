# Financial Advisor AI Lab

An educational software project for learning AI technologies through a small financial-advisor simulation. The application is a practical laboratory, not a production financial-advice service.

## Project documents

- [Project charter](docs/project-charter.md): objectives, scope, and boundaries.
- [Architecture](docs/architecture.md): confirmed stack direction, proposed structure, dependencies, and open decisions.
- [Learning roadmap](docs/learning-roadmap.md): industry-prioritised categories, flexible sequencing, and progress tracking.
- [Development principles](docs/development-principles.md): incremental workflow and project practices.
- [Codex instructions](AGENTS.md): persistent instructions for AI coding agents working in this repository.

## Current status

The first learning slice is a small React page backed by a Python FastAPI API and PostgreSQL. It lists records from the `Test` table; the API initializes the table and inserts one synthetic sample row when the table is empty. See [architecture](docs/architecture.md) and [learning roadmap](docs/learning-roadmap.md) for the confirmed scope and experiment status.

## Run locally

1. Ensure PostgreSQL is running with the `financial_advisor_lab` database and `financial_advisor_app` login. Copy `backend/.env.example` to `backend/.env` if needed, then set `DB_PASSWORD` there.
2. In a terminal, from `backend/`, create and install into a virtual environment, then start the API:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

3. In a second terminal, from `frontend/`, install packages and start the page:

   ```powershell
   npm install
   npm run dev
   ```

Use synthetic data only.
