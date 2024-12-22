import os

# Set testing environment variables BEFORE any other imports
os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_DB"] = "0"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"
os.environ["SKIP_GOOGLE_AUTH"] = "true" 