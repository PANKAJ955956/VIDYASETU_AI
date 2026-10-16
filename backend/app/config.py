from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "VidyaSetu AI"
    environment: str = "development"
    database_url: str = "sqlite:///./vidyasetu.db"
    jwt_secret_key: str = "change-this-development-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    frontend_url: str = "http://localhost:5173"
    ai_provider: str = "mock"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
