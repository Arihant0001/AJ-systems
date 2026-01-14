import logging
import json
import urllib.request
import urllib.error

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Production-ready email service using Brevo HTTP API.
    
    SMTP is blocked on many free hosting platforms (Render, Heroku, etc.)
    so we use Brevo's HTTP API instead which works everywhere.
    
    Environment Variables Required:
    - BREVO_API_KEY: Your Brevo API key (starts with 'xkeysib-')
    - FROM_EMAIL: Sender email address
    - FRONTEND_URL: Your frontend URL for reset links
    """
    
    def _get_api_key(self) -> str | None:
        """Get Brevo API key from SMTP_PASSWORD or BREVO_API_KEY"""
        # Try BREVO_API_KEY first, then fall back to SMTP_PASSWORD
        api_key = getattr(settings, 'brevo_api_key', None) or settings.smtp_password
        if api_key and (api_key.startswith('xkeysib-') or api_key.startswith('xsmtpsib-')):
            return api_key
        return None
    
    def _send_via_brevo_api(self, to_email: str, subject: str, html_body: str, text_body: str) -> bool:
        """
        Send email via Brevo HTTP API.
        Returns True on success, False on failure.
        """
        api_key = self._get_api_key()
        if not api_key:
            logger.warning("Brevo API key not configured")
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
            
            data = json.dumps(payload).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, method='POST')
            req.add_header('Accept', 'application/json')
            req.add_header('Content-Type', 'application/json')
            req.add_header('api-key', api_key)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status in (200, 201):
                    logger.info(f"Email sent successfully to {to_email} via Brevo API")
                    return True
                else:
                    logger.error(f"Brevo API returned status {response.status}")
                    return False
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else 'No details'
            logger.error(f"Brevo API HTTP error {e.code}: {error_body}")
            return False
        except urllib.error.URLError as e:
            logger.error(f"Brevo API URL error: {e.reason}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email via Brevo API: {e}")
            return False
    
    def _log_to_console(self, to_email: str, subject: str, reset_link: str) -> None:
        """Fallback: Print email to console in development"""
        print("\n" + "="*60)
        print("📧 PASSWORD RESET EMAIL (Dev Mode)")
        print("="*60)
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print("-"*60)
        print("Hello,")
        print("")
        print("You requested a password reset for your AJ Systems account.")
        print("")
        print("Click the link below to reset your password:")
        print(f"\n{reset_link}\n")
        print(f"This link will expire in {settings.reset_token_expire_minutes} minutes.")
        print("")
        print("If you didn't request this, please ignore this email.")
        print("="*60 + "\n")
    
    def send_password_reset_email(self, email: str, token: str) -> None:
        """
        Send password reset email with secure token link.
        Uses Brevo HTTP API (works on all hosting platforms).
        Falls back to console output if API key not configured.
        """
        reset_link = f"{settings.frontend_url}/reset-password?token={token}"
        subject = "Reset Your Password - AJ Systems"
        
        # Plain text version
        text_body = f"""Hello,

You requested a password reset for your AJ Systems account.

Click the link below to reset your password:
{reset_link}

This link will expire in {settings.reset_token_expire_minutes} minutes.

If you didn't request this password reset, please ignore this email. Your password will remain unchanged.

— AJ Systems Team
"""
        
        # HTML version
        html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: #f8fafc; border-radius: 8px; padding: 32px; text-align: center;">
        <h1 style="color: #1e293b; font-size: 24px; margin-bottom: 16px;">Reset Your Password</h1>
        
        <p style="color: #64748b; margin-bottom: 24px;">
            You requested a password reset for your AJ Systems account.
        </p>
        
        <a href="{reset_link}" 
           style="display: inline-block; background: #0f172a; color: #ffffff; padding: 14px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-bottom: 24px;">
            Reset Password
        </a>
        
        <p style="color: #94a3b8; font-size: 14px; margin-top: 24px;">
            This link will expire in {settings.reset_token_expire_minutes} minutes.
        </p>
        
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;">
        
        <p style="color: #94a3b8; font-size: 12px;">
            If you didn't request this password reset, please ignore this email.<br>
            Your password will remain unchanged.
        </p>
    </div>
    
    <p style="color: #94a3b8; font-size: 12px; text-align: center; margin-top: 16px;">
        — AJ Systems
    </p>
</body>
</html>
"""
        
        # Try Brevo HTTP API first, fall back to console
        if not self._send_via_brevo_api(email, subject, html_body, text_body):
            self._log_to_console(email, subject, reset_link)
        
        logger.info(f"Password reset email processed for {email}")


email_service = EmailService()
