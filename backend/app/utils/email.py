import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Production-ready email service using SMTP.
    
    Supports Brevo (Sendinblue) free tier:
    - 300 emails/day free
    - SMTP Server: smtp-relay.brevo.com
    - Port: 587
    - Get API Key: https://app.brevo.com/settings/keys/smtp
    
    Environment Variables Required:
    - SMTP_HOST=smtp-relay.brevo.com
    - SMTP_PORT=587
    - SMTP_USER=apikey
    - SMTP_PASSWORD=<your-brevo-api-key>
    - FROM_EMAIL=no-reply@yourdomain.com
    - FRONTEND_URL=https://your-frontend.vercel.app
    """
    
    def _is_smtp_configured(self) -> bool:
        """Check if SMTP credentials are configured"""
        return bool(settings.smtp_user and settings.smtp_password)
    
    def _send_email(self, to_email: str, subject: str, html_body: str, text_body: str) -> bool:
        """
        Send email via SMTP.
        Returns True on success, False on failure.
        """
        if not self._is_smtp_configured():
            logger.warning("SMTP not configured, falling back to console output")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{settings.from_name} <{settings.from_email}>"
            msg['To'] = to_email
            
            # Attach both plain text and HTML versions
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Create secure connection
            context = ssl.create_default_context()
            
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}")
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
        Falls back to console output if SMTP is not configured.
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
        
        # HTML version (clean, simple, works on all email clients)
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
        
        # Try to send via SMTP, fall back to console
        if not self._send_email(email, subject, html_body, text_body):
            self._log_to_console(email, subject, reset_link)
        
        logger.info(f"Password reset email processed for {email}")


email_service = EmailService()
