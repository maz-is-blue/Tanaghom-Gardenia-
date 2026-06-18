"""Application configuration, loaded from environment variables."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # dotenv is optional outside local dev
    pass


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.environ.get("MONGO_DB", "tanaghom_gardenia")
    # Comma-separated list of allowed CORS origins for the JSON API ("*" = any)
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
