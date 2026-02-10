"""Configuration settings for the application."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration sourced from environment variables."""

    GROQ_API_KEY: str


settings = Settings()
