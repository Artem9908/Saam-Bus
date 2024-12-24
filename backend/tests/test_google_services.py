import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.google_docs import GoogleDocsService
from app.services.google_drive import GoogleDriveService
from app.services.document import DocumentService
from datetime import datetime
from app.config import SKIP_GOOGLE_AUTH
from app.models import GeneratedDocument
import os
from app.exceptions import GoogleAPIError

@pytest.fixture
def google_docs_service():
    return GoogleDocsService()

@pytest.fixture
def google_drive_service():
    return GoogleDriveService()

@pytest.fixture
def document_service():
    return DocumentService()

@pytest.fixture
def mock_google_docs(mocker):
    """Mock Google Docs service"""
    mock = mocker.patch('app.services.google_docs.GoogleDocsService', autospec=True)
    mock_instance = mock.return_value
    mock_instance.create_document.return_value = {
        'doc_id': 'mock-id',
        'doc_url': 'https://docs.google.com/document/d/mock-id'
    }
    return mock_instance

@patch('os.getenv')
@patch('os.path.exists')
@patch('google.oauth2.service_account.Credentials.from_service_account_file')
def test_mock_document_creation(mock_creds, mock_exists, mock_getenv):
    """Test document creation in mock mode"""
    # Set up mock environment
    mock_getenv.side_effect = lambda x, *args: {
        'GOOGLE_CREDENTIALS_PATH': 'path/to/credentials.json',
        'GOOGLE_API_USE_CLIENT_CERTIFICATE': 'false'
    }.get(x, args[0] if len(args) > 0 else None)
    
    mock_exists.return_value = True
    mock_creds.return_value = MagicMock()

    # Create service with mocked credentials
    service = GoogleDocsService()
    
    # Add assertions
    assert service.docs_service is not None
    assert service.drive_service is not None

def test_google_docs_initialization():
    """Test service initialization"""
    service = GoogleDocsService()
    assert service is not None
    if SKIP_GOOGLE_AUTH:
        # Service should be mocked in test environment
        assert isinstance(service.docs_service, Mock)
    else:
        assert service.docs_service is not None

def test_google_drive_initialization():
    """Test Google Drive service initialization"""
    service = GoogleDriveService()
    assert service is not None
    # Changed assertion to check if service is properly initialized
    assert service.service is not None

@pytest.mark.asyncio
async def test_google_drive_upload_document(mocker):
    """Test document upload with mocks"""
    # Mock credentials and service setup
    mock_creds = mocker.patch('google.oauth2.service_account.Credentials.from_service_account_file')
    mock_creds.return_value = MagicMock()
    mocker.patch('os.path.exists', return_value=True)

    # Create mock response
    mock_file = {'id': 'test123', 'webViewLink': 'http://mock-drive.com/test123'}
    mock_create = MagicMock()
    mock_create.execute.return_value = mock_file

    # Set up service mock
    mock_files = MagicMock()
    mock_files.create.return_value = mock_create

    mock_service = MagicMock()
    mock_service.files.return_value = mock_files

    # Create service instance and inject mock
    service = GoogleDriveService()
    service.service = mock_service

    # Test upload
    result = await service.upload_document("Test content", "test.txt")
    
    assert result['doc_id'] == 'test123'
    assert result['doc_url'] == 'http://mock-drive.com/test123'

@pytest.mark.asyncio
async def test_google_drive_upload(mocker):
    """Test actual document upload with proper mocking"""
    # Mock credentials and service setup
    mock_creds = mocker.patch('google.oauth2.service_account.Credentials.from_service_account_file')
    mock_creds.return_value = MagicMock()
    mocker.patch('os.path.exists', return_value=True)

    # Mock response
    mock_response = {'id': 'test123', 'webViewLink': 'http://mock-drive.com/test123'}
    
    # Create mock chain
    mock_create = MagicMock()
    mock_create.execute.return_value = mock_response
    
    mock_files = MagicMock()
    mock_files.create.return_value = mock_create
    
    mock_service = MagicMock()
    mock_service.files.return_value = mock_files

    # Create service and inject mock
    service = GoogleDriveService()
    service.service = mock_service

    # Test upload
    result = await service.upload_document("Test content", "test.txt")
    
    assert result['doc_id'] == 'test123'
    assert result['doc_url'] == 'http://mock-drive.com/test123'

@pytest.mark.asyncio
async def test_document_service_generate_content(document_service):
    """Test document content generation"""
    name = "Test User"
    date = "2024-01-01"
    amount = 100.50
    
    result = await document_service.generate_document_content(
        name=name,
        date=date,
        amount=amount,
        template_type="receipt"
    )
    
    assert isinstance(result, dict)
    assert 'content' in result
    assert 'doc_url' in result
    assert 'doc_id' in result

@pytest.mark.asyncio
async def test_document_service_get_documents(document_service, test_db):
    """Test getting documents with filters"""
    # Clear existing documents
    test_db.query(GeneratedDocument).delete()
    test_db.commit()
    
    # Create test documents
    docs = [
        GeneratedDocument(
            name=f"Test User {i}",
            date=datetime.now().date(),
            amount=100.50 + i,
            content=f"Test content {i}",
            doc_id=f"mock-{i}"
        ) for i in range(2)
    ]
    test_db.add_all(docs)
    test_db.commit()

    result = await document_service.get_documents(test_db)
    assert result['total'] == 2
    assert len(result['items']) == 2

@pytest.mark.asyncio
async def test_google_api_error_handling(document_service):
    """Test Google API error handling"""
    # Configure mock to raise error
    document_service.google_docs.docs_service.documents.return_value.create.side_effect = GoogleAPIError("API Error")
    
    with pytest.raises(GoogleAPIError, match="API Error"):
        await document_service.generate_document_content(
            name="Test",
            date="2024-01-01",
            amount=100.0,
            template_type="receipt"
        )

@pytest.mark.asyncio
async def test_google_docs_service_error_handling():
    """Test Google Docs service error handling"""
    service = GoogleDocsService()
    
    # Configure mock to raise error
    service.docs_service.documents.return_value.create.side_effect = GoogleAPIError("API connection failed")
    
    with pytest.raises(GoogleAPIError, match="API connection failed"):
        await service.create_document("Test content")