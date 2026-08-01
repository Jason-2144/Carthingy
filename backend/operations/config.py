from pydantic_settings import BaseSettings

class OperationsSettings(BaseSettings):
    # JWT Auth
    JWT_SECRET_KEY: str = "super_secret_jwt_key_replace_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_MINUTES: int = 15
    
    # Emails
    SMTP_HOST: str = "smtp.mailtrap.io"
    SMTP_PORT: int = 587
    SMTP_USER: str = "user"
    SMTP_PASSWORD: str = "password"
    FROM_EMAIL: str = "noreply@carscope.ai"
    
    # Redis for Notifications/Audit/Rate Limiting
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_prefix = "OPS_"

ops_settings = OperationsSettings()
