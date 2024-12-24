from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import os

from app.main import app
from app.database import Base, get_db
from app.services.document import DocumentService
from app.services.cache import RedisCache

# Ensure TESTING is set to true
os.environ["TESTING"] = "true"

# Use in-memory SQLite for tests
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"

# Mock services
class MockRedisCache:
    def __init__(self):
        self._cache = {}

    async def get(self, key: str):
        return self._cache.get(key)

    async def set(self, key: str, value: str, expiration: int = 300):
        self._cache[key] = value

class MockDocumentService:
    async def generate_document_content(self, name, date, amount, template_type):
        return {
            'name': name,
            'date': date,
            'amount': amount,
            'content': 'Mock content',
            'doc_id': 'mock-doc-id',
            'doc_url': 'https://docs.google.com/document/d/mock-doc-id/edit'
        }

# Override dependencies for testing
def override_get_cache():
    return MockRedisCache()

def override_get_document_service():
    return MockDocumentService()

# Setup test app
def get_test_app():
    app.dependency_overrides[get_cache_service] = override_get_cache
    app.dependency_overrides[get_document_service] = override_get_document_service
    return app 