import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Explicitly point to the .env file at the project root
ENV_FILE = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    """
    Central configuration class.
    Automatically loads variables from the environment and .env file.
    """
    # NewsAPI
    NEWS_API_KEY: str = ""
    NEWS_QUERY: str = "stocks OR markets OR economy"

    # LLM
    OPENAI_API_KEY: str = ""

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    TARGET_EMAIL: str = ""

    # App
    SCHEDULE_TIME: str = "06:00"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore"
    )

config = Settings()
