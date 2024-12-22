import os

# Environment variables
TESTING = os.getenv("TESTING", "false").lower() == "true"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/saam")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Google
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
SKIP_GOOGLE_AUTH = os.getenv("SKIP_GOOGLE_AUTH", "false").lower() == "true"

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") 