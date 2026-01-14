from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    env: str = "dev"
    database_url: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7

    cors_origins: str = "*"

    # SMTP Configuration for Password Reset Emails (Brevo Free Tier)
    smtp_host: str = "smtp-relay.brevo.com"
    smtp_port: int = 587
    smtp_user: str = ""  # Set to "apikey" for Brevo
    smtp_password: str = ""  # Your Brevo SMTP API key
    from_email: str = "no-reply@ajsystems.app"
    from_name: str = "AJ Systems"
    
    # Frontend URL for reset links
    frontend_url: str = "http://localhost:5173"
    
    # Password reset token expiry in minutes
    reset_token_expire_minutes: int = 30


settings = Settings()  # type: ignore[call-arg]
