import logging
import json
import urllib.request
import urllib.error

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Production-ready email service using Brevo HTTP API.
    """
    
    def _get_api_key(self) -> str | None:
        """Get Brevo API key"""
        api_key = settings.brevo_api_key or settings.smtp_password
        print(f"🔑 API key configured: {bool(api_key)}, starts with: {api_key[:10] if api_key else 'None'}...")
        return api_key if api_key else None
    
    def _send_via_brevo_api(self, to_email: str, subject: str, html_body: str, text_body: str) -> bool:
        """
        Send email via Brevo HTTP API.
        Returns True on success, False on failure.
        """
        api_key = self._get_api_key()
        if not api_key:
            print("❌ Brevo API key not configured!")
            return False
        
        try:
            url = "https://api.brevo.com/v3/smtp/email"
            
            payload = {
                "sender": {
                    "name": settings.from_name,
                    "email": settings.from_email
                },
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html_body,
                "textContent": text_body
            }
            
            print(f"📧 Sending email to {to_email} from {settings.from_email}")
            
            data = json.dumps(payload).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, method='POST')
            req.add_header('Accept', 'application/json')
            req.add_header('Content-Type', 'application/json')
            req.add_header('api-key', api_key)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                response_body = response.read().decode('utf-8')
                print(f"Brevo API response: {response.status} - {response_body}")
                if response.status in (200, 201):
                    print(f"✅ Email sent successfully to {to_email} via Brevo API")
                    return True
                else:
                    print(f"❌ Brevo API returned status {response.status}")
                    return False
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else 'No details'
            print(f"❌ Brevo API HTTP error {e.code}: {error_body}")
            return False
        except urllib.error.URLError as e:
            print(f"❌ Brevo API URL error: {e.reason}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error sending email via Brevo API: {e}")
            return False
    
    def _log_to_console(self, to_email: str, subject: str, reset_link: str) -> None:
        """Fallback: Print email to console in development"""
        print("\n" + "="*60)
        print("📧 PASSWORD RESET EMAIL (Dev Mode - API Failed)")
        print("="*60)
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print("-"*60)
        print(f"Reset Link: {reset_link}")
        print("="*60 + "\n")
    
    def send_password_reset_email(self, email: str, token: str) -> None:
        """
        Send password reset email with secure token link.
        """
        reset_link = f"{settings.frontend_url}/reset-password?token={token}"
        subject = "Reset Your Password - AJ Systems"
        
        text_body = f"""Hello,

You requested a password reset for your AJ Systems account.

Click the link below to reset your password:
{reset_link}

This link will expire in {settings.reset_token_expire_minutes} minutes.

If you didn't request this, ignore this email.

— AJ Systems Team
"""
        
        html_body = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: #f8fafc; border-radius: 8px; padding: 32px; text-align: center;">
        <h1 style="color: #1e293b;">Reset Your Password</h1>
        <p style="color: #64748b;">You requested a password reset for your AJ Systems account.</p>
        <a href="{reset_link}" style="display: inline-block; background: #0f172a; color: #fff; padding: 14px 32px; text-decoration: none; border-radius: 6px; font-weight: 600;">Reset Password</a>
        <p style="color: #94a3b8; font-size: 14px; margin-top: 24px;">This link expires in {settings.reset_token_expire_minutes} minutes.</p>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;">
        <p style="color: #94a3b8; font-size: 12px;">If you didn't request this, ignore this email.</p>
    </div>
</body>
</html>"""
        
        print(f"=== Starting password reset email to {email} ===")
        
        if self._send_via_brevo_api(email, subject, html_body, text_body):
            print(f"=== Email sent successfully ===")
        else:
            print(f"=== Email sending failed, showing in console ===")
            self._log_to_console(email, subject, reset_link)


email_service = EmailService()
