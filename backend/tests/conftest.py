from . import test_env  # This must be the first import
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime
from httpx import AsyncClient
import aioredis

# Import app modules after environment is set
from app.database import Base, get_db
from app.main import app
from app.models import GeneratedDocument

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
async def async_client(test_db):
    """Create async test client with database dependency."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
def sample_document(test_db):
    """Create a sample document in the database"""
    doc = GeneratedDocument(
        name="Test User",
        date=datetime.now().date(),
        amount=100.50,
        content="Test content"
    )
    test_db.add(doc)
    test_db.commit()
    test_db.refresh(doc)
    return doc