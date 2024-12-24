import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Testing
TESTING = os.getenv("TESTING", "false").lower() == "true"
SKIP_GOOGLE_AUTH = os.getenv("SKIP_GOOGLE_AUTH", "false").lower() == "true"

# Set this before any other Google-related configs
os.environ['GOOGLE_API_USE_CLIENT_CERTIFICATE'] = 'false'

# Google Drive Configuration
GOOGLE_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_CREDENTIALS_PATH", 
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials/saam-bus-2143aa7b9c18.json')
)
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")

# Ensure credentials directory exists
credentials_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials')
os.makedirs(credentials_dir, exist_ok=True)

# Database
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "saam")

# Set default DATABASE_URL
if TESTING:
    DATABASE_URL = "sqlite:///:memory:?check_same_thread=False"
else:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/saam"
    )

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# Development
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "true").lower() == "true"