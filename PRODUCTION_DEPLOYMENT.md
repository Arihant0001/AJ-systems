# 🚀 AJ Systems - Production Deployment (FREE SaaS PWA)

**Your app is ready to deploy!** Follow this guide to launch on **Vercel** (frontend), **Render** (backend), and **Supabase** (database) — completely free.

---

## 🎯 What You're Deploying

✅ **Frontend:** React + TypeScript web app with PWA support  
✅ **Backend:** FastAPI REST API with JWT auth  
✅ **Database:** PostgreSQL with migrations  
✅ **Email:** Forgot password flow with SMTP  
✅ **Installable:** "Add to Home Screen" on mobile  

---

## 📊 Free Services Stack

| Component | Service | URL | Cold Start |
|-----------|---------|-----|-----------|
| **Frontend** | Vercel | `https://aj-systems.vercel.app` | None (instant) |
| **Backend API** | Render | `https://aj-systems-api.onrender.com` | 30 seconds (free tier) |
| **Database** | Supabase | PostgreSQL | None (instant) |
| **Email** | Brevo | SMTP Relay | None (instant) |

**Total Cost: $0/month** 🎉

---

## 🚨 IMPORTANT BEFORE STARTING

**Read these 3 files in order:**

1. **[DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)** ← Phase checklist  
2. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** ← Step-by-step instructions  
3. **[BREVO_SETUP.md](BREVO_SETUP.md)** ← Email configuration  

---

## ⚡ 60-Second Quick Start

### Step 1: GitHub Repository Setup
```bash
# Navigate to project root
cd tundler-app-demo

# Create .gitignore (already done, just verify)
git init
git add .
git commit -m "Initial commit: production-ready SaaS app"
git remote add origin https://github.com/YOUR-USERNAME/aj-systems.git
git branch -M main
git push -u origin main
```

### Step 2: Supabase Database (15 min)
1. Go to [supabase.com](https://supabase.com) → Sign up → Create project
2. Copy **Connection String** → Save to `backend/.env` as `DATABASE_URL`
3. Run locally: `cd backend && alembic upgrade head`
4. ✅ Database ready

### Step 3: Render Backend (20 min)
1. Go to [render.com](https://render.com) → Connect GitHub
2. Create **Web Service** from repo
3. Set start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 10000`
4. Add env vars (from `.env.production` template)
5. Deploy
6. ✅ API live at `https://aj-systems-api.onrender.com`

### Step 4: Vercel Frontend (10 min)
1. Go to [vercel.com](https://vercel.com) → Import project
2. Select `frontend` as root directory
3. Add env var: `VITE_API_URL=https://aj-systems-api.onrender.com`
4. Deploy
5. ✅ Frontend live at `https://aj-systems.vercel.app`

### Step 5: Test It
- 📱 Visit `https://aj-systems.vercel.app`
- 🔐 Signup / Login / Forgot Password
- 📊 Add persons, adjust tiffin counts
- 📲 Android/iOS: Tap menu → Install app

---

## 🎓 What Each Phase Does

| Phase | What | Time | Free |
|-------|------|------|------|
| 1️⃣ Verification | Confirm app works locally | 5 min | N/A |
| 2️⃣ Supabase | Setup PostgreSQL database | 15 min | ✅ Yes |
| 3️⃣ Render | Deploy API server | 20 min | ✅ Yes |
| 4️⃣ Vercel | Deploy web frontend | 10 min | ✅ Yes |
| 5️⃣ PWA | Enable app installation | 5 min | ✅ Yes |
| 6️⃣ Testing | Verify everything works | 15 min | N/A |
| 7️⃣ Safety | Check failure modes | 5 min | N/A |

**Total Time: ~75 minutes** ⏱️

---

## 📋 Pre-Deployment Checklist

**Before you start, verify locally:**

- [ ] Backend runs: `cd backend && uvicorn app.main:app --reload`
- [ ] Frontend runs: `cd frontend && npm run dev`
- [ ] Login works
- [ ] Forgot password page accessible
- [ ] No errors in browser console
- [ ] `.env` is in `.gitignore`
- [ ] No secrets in code

Run check script:
```bash
bash scripts/pre-deploy-check.sh
```

---

## 🔑 Key Credentials You'll Need

**Create accounts for:**

1. **GitHub** - For code storage (free)
2. **Supabase** - For database (free PostgreSQL)
3. **Render** - For backend server (free)
4. **Vercel** - For frontend hosting (free)
5. **Brevo** - For password reset emails (free 300/day)

All accounts have **free forever** tiers.

---

## 🆘 Common Issues & Solutions

### "Backend not responding"
- Check Render deployment logs
- Free tier has 30-second cold start (normal!)
- First request after 15 min idle takes time

### "Can't connect to Supabase"
- Verify `DATABASE_URL` in env vars
- Check database exists in Supabase dashboard
- Confirm connection string format

### "Frontend shows API errors"
- Check `VITE_API_URL` env var matches backend URL
- Verify backend CORS includes frontend domain
- Check browser console for actual error

### "Password reset email not sending"
- Verify Brevo credentials in backend env vars
- Check Brevo account is activated
- Verify email address is correct

---

## 📖 Full Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Detailed step-by-step for all phases
- **[DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)** - Checklist & status tracking
- **[BREVO_SETUP.md](BREVO_SETUP.md)** - Email service configuration
- **[PASSWORD_RESET_GUIDE.md](PASSWORD_RESET_GUIDE.md)** - Password reset implementation details

---

## ✨ After Deployment

### Monitor Your App
- **Render Logs:** Check backend errors in real-time
- **Vercel Analytics:** See frontend performance
- **Supabase Dashboard:** View database usage
- **GitHub:** All deployments track to your git commits

### Scale (When Needed)
- Backend cold starts annoying? Upgrade Render to **$7/month** → eliminate cold starts
- Database > 500 MB? Upgrade Supabase → pay per usage
- Everything else free ✅

### User Release Statement
```
AJ Systems is now live at https://aj-systems.vercel.app

📱 Install on your phone:
- Tap menu in Chrome/Safari
- Select "Add to Home Screen"
- App appears on home screen like native app

🎉 No Play Store required!
```

---

## 🎯 Next Steps

1. **Read** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. **Create** accounts on Supabase, Render, Vercel, Brevo
3. **Follow** phase-by-phase instructions
4. **Test** signup/login/forgot password
5. **Share** link with users!

---

## 💬 Questions?

- Render docs: [render.com/docs](https://render.com/docs)
- Supabase docs: [supabase.com/docs](https://supabase.com/docs)
- Vercel docs: [vercel.com/docs](https://vercel.com/docs)
- Brevo docs: [brevo.com/docs](https://brevo.com/docs)

---

**Let's deploy! 🚀**

Start with [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) Phase 2: Supabase Database
