# Tundler Backend (FastAPI)

## Local dev

1. Create a `.env` from `.env.example`
2. Install deps

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run migrations (needs Postgres running)

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

4. Start API

```bash
uvicorn app.main:app --reload --port 8000
```

## Deploy

- Backend: Render or Railway
- DB: Neon or Supabase Postgres
- Configure env vars from `.env.example`
