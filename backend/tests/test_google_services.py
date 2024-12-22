import pytest
from unittest.mock import Mock, patch
from app.services.google_docs import GoogleDocsService
from app.services.google_drive import GoogleDriveService
from app.services.document import DocumentService
from datetime import datetime
from app.config import SKIP_GOOGLE_AUTH

@pytest.fixture
def google_docs_service():
    return GoogleDocsService()

@pytest.fixture
def google_drive_service():
    return GoogleDriveService()

@pytest.fixture
def document_service():
    return DocumentService()

def test_mock_document_creation(google_docs_service):
    """Test document creation in mock mode"""
    assert SKIP_GOOGLE_AUTH is True
    doc_id = google_docs_service.create_document("Test", "Content")
    assert doc_id == "mock-doc-id-123"

def test_google_docs_initialization():
    """Test service initialization"""
    service = GoogleDocsService()
    assert service is not None
    if SKIP_GOOGLE_AUTH:
        assert service.docs_service is None
    else:
        assert service.docs_service is not None

def test_google_drive_initialization():
    """Test Google Drive service initialization in test mode"""
    service = GoogleDriveService()
    assert service is not None
    # In test mode, service should not be initialized
    assert service.service is None

@patch('os.getenv')
def test_google_drive_upload_document(mock_getenv):
    """Test document upload in test mode"""
    service = GoogleDriveService()
    filename = "test.txt"
    link = service.upload_document("Test content", filename)
    assert link == f"http://mock-drive-link.com/{filename}"

def test_document_service_generate_content(document_service):
    """Test document content generation"""
    name = "Test User"
    date = "2024-01-01"
    amount = 100.50
    
    result = document_service.generate_document_content(name, date, amount)
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "doc_url" in result
    assert "doc_id" in result
    assert result["doc_id"] == "mock-id-123"
    assert "Test User" in result["content"]
    assert "100.50" in result["content"]
    assert "2024-01-01" in result["content"]

@pytest.mark.asyncio
async def test_document_service_get_documents(document_service, test_db):
    """Test getting documents with filters"""
    # Create test documents
    from app.models import GeneratedDocument
    doc1 = GeneratedDocument(
        name="Test User 1",
        date=datetime.now().date(),
        amount=100.50,
        content="Test content 1",
        doc_id="mock-1"
    )
    doc2 = GeneratedDocument(
        name="Test User 2",
        date=datetime.now().date(),
        amount=200.50,
        content="Test content 2",
        doc_id="mock-2"
    )
    test_db.add(doc1)
    test_db.add(doc2)
    test_db.commit()

    # Test without filters
    docs = await document_service.get_documents(test_db)
    assert len(docs) == 2

    # Test with name filter
    docs = await document_service.get_documents(test_db, name="User 1")
    assert len(docs) == 1
    assert docs[0]["name"] == "Test User 1"

    # Test with date filter
    today = datetime.now().date().strftime("%Y-%m-%d")
    docs = await document_service.get_documents(test_db, date=today)
    assert len(docs) == 2

    # Test with invalid date
    docs = await document_service.get_documents(test_db, date="invalid-date")
    assert len(docs) == 2  # Should ignore invalid date

@patch('google.oauth2.service_account.Credentials.from_service_account_file')
def test_google_docs_service_error_handling(mock_credentials):
    """Test error handling in Google Docs service"""
    mock_credentials.side_effect = Exception("Auth error")
    service = GoogleDocsService()
    assert service.docs_service is None
    assert service.drive_service is None