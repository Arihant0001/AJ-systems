# 📧 Brevo (Sendinblue) Setup Guide

Free email service for password reset notifications.

## Step 1: Create Free Brevo Account

1. Go to [brevo.com](https://brevo.com)
2. Click **"Sign Up for Free"**
3. Enter email and password
4. Confirm email address

## Step 2: Get SMTP Credentials

1. In Brevo dashboard, go **Settings → SMTP & API**
2. Under "Transactional Email," find:
   - **SMTP Server:** `smtp-relay.brevo.com`
   - **Port:** `587`
   - **Username:** Your Brevo login email
   - **Password:** Generate "SMTP Key" (copy immediately)

## Step 3: Configure in Backend

Add to `backend/.env`:

```env
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=xsmtpNABC123XYZ...
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=AJ Systems
```

## Step 4: Update Python Code

Edit [backend/app/utils/email.py](backend/app/utils/email.py):

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_password_reset_email(email: str, reset_url: str) -> bool:
    """Send password reset email via Brevo SMTP"""
    
    subject = "Reset Your AJ Systems Password"
    
    html_content = f"""
    <h2>Password Reset Request</h2>
    <p>Click the link below to reset your password:</p>
    <p><a href="{reset_url}">Reset Password</a></p>
    <p>This link expires in 30 minutes.</p>
    <p>If you didn't request this, ignore this email.</p>
    """
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.smtp_from_email
        msg["To"] = email
        
        msg.attach(MIMEText(html_content, "html"))
        
        # Send via Brevo
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.smtp_from_email, [email], msg.as_string())
        
        print(f"✅ Reset email sent to {email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
```

Update [backend/app/core/config.py](backend/app/core/config.py):

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    env: str = "dev"
    database_url: str
    
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7
    
    cors_origins: str = ""
    
    # Email settings
    smtp_host: str = "smtp-relay.brevo.com"
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    smtp_from_email: str = "noreply@example.com"
    smtp_from_name: str = "AJ Systems"
```

## Step 5: Test Email Sending

```bash
cd backend

# Test script
python -c "
from app.utils.email import send_password_reset_email
result = send_password_reset_email(
    'your-test-email@example.com',
    'https://aj-systems.vercel.app/reset-password?token=test123'
)
print('Email sent!' if result else 'Email failed!')
"
```

## Step 6: Verify Sending Status

In Brevo dashboard:
1. Go **Campaigns → Transactional**
2. View sent emails and status
3. Check bounce rate and complaints

## Free Tier Limits

- ✅ 300 emails per day
- ✅ Unlimited contacts
- ✅ Basic analytics
- ❌ No custom domain (use default sender)

## Scale When Ready

Upgrade to paid when you exceed 300 emails/day:
- 2000 emails/month: $20/month
- 10000 emails/month: $40/month
- Unlimited: $300/month

No code changes needed - just update credentials.

---

## Quick Reference

| Setting | Value |
|---------|-------|
| Host | `smtp-relay.brevo.com` |
| Port | `587` |
| Security | TLS |
| From Email | Your Brevo email |
| API Key | Generate in Brevo dashboard |
