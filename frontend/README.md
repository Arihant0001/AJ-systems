# Tundler Frontend (React + Vite + Tailwind)

## Local dev

1. Create `.env` from `.env.example`

```bash
VITE_API_URL=http://localhost:8000
```

2. Install + run

```bash
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Deploy (Vercel Free)

- Framework preset: Vite
- Build command: `npm run build`
- Output directory: `dist`
- Env var: `VITE_API_URL=https://<your-backend-domain>`

## Notes

- Auth token is stored in localStorage.
- All API calls include `Authorization: Bearer <token>`.
