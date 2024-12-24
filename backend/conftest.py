import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app

# Set testing environment variables
os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///:memory:?check_same_thread=False"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_DB"] = "0"
os.environ["SKIP_GOOGLE_AUTH"] = "true"

# Your existing fixtures...