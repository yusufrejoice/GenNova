import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # SMTP (Gmail)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_EMAIL: str
    SMTP_PASSWORD: str

    # Hugging Face
    HF_TOKEN: str


    # WaveSpeed
    WAVESPEED_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
