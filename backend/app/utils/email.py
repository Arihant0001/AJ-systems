import logging
from typing import Any

logger = logging.getLogger(__name__)

class EmailService:
    """
    Email service for sending password reset emails.
    
    PRODUCTION SETUP:
    -----------------
    For production, integrate with an SMTP service:
    
    Option 1: Gmail SMTP (Free tier)
    - SMTP Server: smtp.gmail.com
    - Port: 587 (TLS)
    - Create App Password: https://myaccount.google.com/apppasswords
    
    Option 2: Brevo (Sendinblue) Free Tier
    - 300 emails/day free
    - SMTP Server: smtp-relay.brevo.com
    - Port: 587
    - Get API Key: https://app.brevo.com/settings/keys/smtp
    
    Option 3: SendGrid Free Tier
    - 100 emails/day free
    - Use sendgrid-python library
    
    Add to .env:
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USER=your-email@gmail.com
    SMTP_PASSWORD=your-app-password
    FROM_EMAIL=noreply@yourdomain.com
    FRONTEND_URL=https://yourdomain.com
    """
    
    def send_password_reset_email(self, email: str, token: str) -> None:
        """
        Sends a password reset email.
        
        CURRENT MODE: Development (Console Output)
        TODO: Integrate SMTP for production
        """
        # For development, print to console
        reset_link = f"http://localhost:5173/reset-password?token={token}"
        
        print("\n" + "="*60)
        print("📧 PASSWORD RESET EMAIL")
        print("="*60)
        print(f"To: {email}")
        print(f"Subject: Reset Your Password - AJ Systems")
        print("-"*60)
        print("Hello,")
        print("")
        print("You requested a password reset for your AJ Systems account.")
        print("")
        print("Click the link below to reset your password:")
        print(f"\n{reset_link}\n")
        print("This link will expire in 30 minutes.")
        print("")
        print("If you didn't request this, please ignore this email.")
        print("="*60 + "\n")
        
        logger.info(f"Password reset email generated for {email}")
        
        # TODO: Production SMTP implementation
        # Example using smtplib:
        #
        # import smtplib
        # from email.mime.text import MIMEText
        # from email.mime.multipart import MIMEMultipart
        #
        # msg = MIMEMultipart('alternative')
        # msg['Subject'] = "Reset Your Password - AJ Systems"
        # msg['From'] = settings.smtp_from_email
        # msg['To'] = email
        #
        # html = f"""
        # <html>
        #   <body>
        #     <h2>Reset Your Password</h2>
        #     <p>Click the link below to reset your password:</p>
        #     <a href="{reset_link}">Reset Password</a>
        #     <p>This link expires in 30 minutes.</p>
        #   </body>
        # </html>
        # """
        #
        # msg.attach(MIMEText(html, 'html'))
        #
        # with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        #     server.starttls()
        #     server.login(settings.smtp_user, settings.smtp_password)
        #     server.send_message(msg)

email_service = EmailService()
