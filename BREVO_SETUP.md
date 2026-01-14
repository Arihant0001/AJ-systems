# 📧 Brevo SMTP Setup Guide

Free email service for password reset (300 emails/day free).

## Quick Setup (5 minutes)

### Step 1: Create Brevo Account

1. Go to [brevo.com](https://brevo.com)
2. Click **"Sign Up for Free"**
3. Verify your email address

### Step 2: Get SMTP API Key

1. Login to Brevo dashboard
2. Go to **Settings → SMTP & API** (or click your profile → SMTP & API)
3. Under **SMTP** section:
   - Click **"Generate a new SMTP Key"**
   - Copy the key immediately (shown only once!)

### Step 3: Add to Render Environment

In your Render backend service, add these environment variables:

| Variable | Value |
|----------|-------|
| `SMTP_HOST` | `smtp-relay.brevo.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | `apikey` |
| `SMTP_PASSWORD` | `xsmtpsib-xxxxx...` (your SMTP key) |
| `FROM_EMAIL` | `no-reply@ajsystems.app` |
| `FROM_NAME` | `AJ Systems` |
| `FRONTEND_URL` | `https://your-app.vercel.app` |

### Step 4: Verify Setup

Test the password reset flow:
1. Go to your app's login page
2. Click "Forgot Password?"
3. Enter your email
4. Check inbox for reset email

---

## Troubleshooting

### Email not received?
- Check spam/junk folder
- Verify SMTP_PASSWORD is correct (regenerate if needed)
- Check Render logs for SMTP errors

### Authentication errors?
- Make sure `SMTP_USER` is exactly `apikey` (not your email)
- Ensure SMTP key starts with `xsmtpsib-`

### Free tier limits
- 300 emails/day
- No credit card required
- Sufficient for most small apps

---

## Local Development

For local testing without SMTP, emails print to console:

```
============================================================
📧 PASSWORD RESET EMAIL (Dev Mode)
============================================================
To: user@example.com
Subject: Reset Your Password - AJ Systems
------------------------------------------------------------
Click the link below to reset your password:

http://localhost:5173/reset-password?token=ABC123...
============================================================
```

To test actual email sending locally, add to `backend/.env`:
```env
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-brevo-smtp-key
FROM_EMAIL=no-reply@yourdomain.com
FRONTEND_URL=http://localhost:5173
```

---

## Security Features Implemented

✅ **No email enumeration** - Same response whether email exists or not  
✅ **Token hashing** - SHA-256 hash stored, plain token sent in email  
✅ **One-time use** - Tokens marked as used after reset  
✅ **Expiry enforced** - 30-minute token validity  
✅ **Rate limiting** - 3 requests per 5 minutes per IP  
✅ **Password strength** - Requires uppercase, lowercase, number, 8+ chars  
✅ **Auto-cleanup** - Expired tokens removed automatically
