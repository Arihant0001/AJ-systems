# Tundler (Multi-tenant SaaS)

Web-only SaaS starter with strict owner-scoped data isolation.

- Frontend: React (Vite) + Tailwind
- Backend: FastAPI + JWT
- DB: PostgreSQL

## Local dev

### 1) Backend

- Copy `backend/.env.example` to `backend/.env`
- Set `DATABASE_URL` to a running Postgres instance

Then:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend

- Copy `frontend/.env.example` to `frontend/.env`

Then:

```bash
cd frontend
npm install
npm run dev
```

## Deployment (Free tiers)

### Database (Neon/Supabase)

- Create a Postgres database
- Copy the connection string into `DATABASE_URL`

### Backend (Render/Railway)

Env vars:

- `DATABASE_URL`
- `JWT_SECRET`
- `JWT_ALGORITHM` (default `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CORS_ORIGINS` (e.g. `https://<vercel-app>.vercel.app`)

Start command:

- `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

Env vars:

- `VITE_API_URL=https://<backend-domain>`

Build:

- `npm run build`

Output:

- `dist`

## Security model

- All protected endpoints require JWT
- All records are owner-scoped by `owner_id`
- Tiffin actions are append-only logs (GIVEN/REVERSED); totals are derived
- PDF is generated dynamically and marked `no-store`
