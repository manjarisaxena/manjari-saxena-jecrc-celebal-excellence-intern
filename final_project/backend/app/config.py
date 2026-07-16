import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "HireSense AI Core Engine"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/hiresense")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

if not settings.JWT_SECRET:
    # Fail loudly rather than silently running with a guessable/shared secret.
    raise RuntimeError(
        "JWT_SECRET is not set. Copy .env.example to .env and set a real secret "
        "before starting the server."
    )
