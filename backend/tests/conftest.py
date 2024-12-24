import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from .test_config import TEST_DATABASE_URL
import os
from app.services.cache_decorator import IN_MEMORY_CACHE

@pytest.fixture(scope="session")
def test_app():
    return app

@pytest.fixture
async def async_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
def test_client(test_app):
    return TestClient(test_app)

@pytest.fixture(scope="session")
def test_db():
    """Create a fresh database for each test session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_test_env():
    """Ensure test environment is properly configured"""
    os.environ["TESTING"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    yield

# ------------------------------------------------------
# New fixtures for "document_service" and "sample_document"
# ------------------------------------------------------
from datetime import datetime
from app.services.document import DocumentService
from app.models import GeneratedDocument

@pytest.fixture
def document_service():
    """Return a DocumentService instance for testing."""
    return DocumentService()

@pytest.fixture
def sample_document(test_db):
    """Create and return a sample document for testing."""
    doc = GeneratedDocument(
        name="Sample Document",
        date=datetime.now().date(),
        amount=123.45,
        content="Sample content"
    )
    test_db.add(doc)
    test_db.commit()
    return doc

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all tables before running tests"""
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear the in-memory cache before each test"""
    from app.services.cache_decorator import IN_MEMORY_CACHE
    IN_MEMORY_CACHE.clear()
    yield