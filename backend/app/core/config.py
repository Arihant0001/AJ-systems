from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    env: str = "dev"
    database_url: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7

    cors_origins: str = "*"

    # SMTP Configuration (kept for backward compatibility)
    smtp_host: str = "smtp-relay.brevo.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""  # Can also be Brevo API key (xkeysib- or xsmtpsib-)
    
    # Brevo API key (preferred - works on all hosting platforms)
    brevo_api_key: str = ""
    
    # Email settings
    from_email: str = "no-reply@ajsystems.app"
    from_name: str = "AJ Systems"
    
    # Frontend URL for reset links
    frontend_url: str = "http://localhost:5173"
    
    # Password reset token expiry in minutes
    reset_token_expire_minutes: int = 30


settings = Settings()  # type: ignore[call-arg]
