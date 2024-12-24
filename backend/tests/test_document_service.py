import pytest
from datetime import datetime
from app.services.document import DocumentService
from app.models import GeneratedDocument
from app.exceptions import ValidationError, GoogleAPIError, DatabaseError, TemplateError

@pytest.mark.asyncio
async def test_document_pagination(document_service, test_db):
    """Test document pagination"""
    # Create 15 test documents
    for i in range(15):
        doc = GeneratedDocument(
            name=f"Test User {i}",
            date=datetime.now().date(),
            amount=100.50 + i,
            content=f"Test content {i}",
            doc_id=f"mock-{i}"
        )
        test_db.add(doc)
    test_db.commit()

    # Test first page
    result = await document_service.get_documents(test_db, page=1, page_size=10)
    assert len(result["items"]) == 10
    assert result["total"] == 15
    assert result["pages"] == 2

    # Test second page
    result = await document_service.get_documents(test_db, page=2, page_size=10)
    assert len(result["items"]) == 5

@pytest.mark.asyncio
async def test_document_validation_errors(document_service):
    """Test document validation errors"""
    with pytest.raises(ValidationError):
        await document_service.generate_document_content(
            name="A",  # Too short
            date="2024-01-01",
            amount=100.50,
            template_type="receipt"
        )

    with pytest.raises(ValidationError, match="Date cannot be in the future"):
        await document_service.generate_document_content(
            name="Test User", 
            date="2025-01-01", 
            amount=100.50,
            template_type="receipt"
        )

    with pytest.raises(ValidationError, match="Amount must be greater than 0"):
        await document_service.generate_document_content(
            "Test User",
            "2024-01-01",
            -100.50,
            "receipt"
        )

    with pytest.raises(ValidationError, match="Amount cannot exceed 1,000,000"):
        await document_service.generate_document_content(
            name="Test User",
            date="2024-01-01",
            amount=1500000.00,
            template_type="receipt"
        )

@pytest.mark.asyncio
async def test_document_service_validation():
    """Test document service validation"""
    service = DocumentService()
    
    # Test template validation
    with pytest.raises(TemplateError, match="Invalid template type. Must be one of: receipt, invoice, contract"):
        service.validate_document_data(
            name="Test User",
            date="2024-01-01",
            amount=100.50,
            template_type="invalid"
        )
    
    # Test amount validation
    with pytest.raises(ValidationError, match="Amount cannot exceed 1,000,000"):
        service.validate_document_data(
            name="Test User",
            date="2024-01-01",
            amount=2000000,
            template_type="receipt"
        )

@pytest.mark.asyncio
async def test_document_generation_with_google_api_error(document_service, mocker):
    """Test document generation when Google API fails"""
    # Mock the Google Docs service to raise a GoogleAPIError
    mocker.patch.object(
        document_service.google_docs,
        'create_document',
        side_effect=GoogleAPIError("Failed to create Google document")
    )
    
    with pytest.raises(GoogleAPIError, match="Failed to create Google document"):
        await document_service.generate_document_content(
            name="Test User",
            date="2024-01-01",
            amount=100.50,
            template_type="receipt"
        )

@pytest.mark.asyncio
async def test_document_service_database_errors(document_service, test_db, mocker):
    """Test database error handling"""
    mocker.patch.object(
        test_db,
        'query',
        side_effect=DatabaseError("Database connection error")
    )
    
    with pytest.raises(DatabaseError, match="Error retrieving documents"):
        await document_service.get_documents(test_db)

@pytest.mark.asyncio
async def test_document_service_google_api_errors(document_service, mocker):
    """Test Google API error handling"""
    mocker.patch.object(
        document_service.google_docs,
        'create_document',
        side_effect=GoogleAPIError("API connection failed")
    )
    
    with pytest.raises(GoogleAPIError, match="API connection failed"):
        await document_service.generate_document_content(
            "Test User",
            "2024-01-01",
            100.50,
            "receipt"
        )

@pytest.mark.asyncio
async def test_invalid_template_type(document_service):
    """Test invalid template type handling"""
    with pytest.raises(TemplateError, match="Invalid template type. Must be one of: receipt, invoice, contract"):
        await document_service.generate_document_content(
            "Test User",
            "2024-01-01",
            100.50,
            "invalid_template"
        )

@pytest.mark.asyncio
async def test_template_error_handling(document_service):
    """Test template error handling"""
    with pytest.raises(TemplateError):
        await document_service.generate_document_content(
            name="Test User",
            date="2024-01-01",
            amount=100.50,
            template_type="invalid"
        )

@pytest.mark.asyncio
async def test_invalid_page_parameters(document_service, test_db):
    """Test invalid pagination parameters"""
    with pytest.raises(ValidationError, match="Page number must be positive"):
        await document_service.get_documents(test_db, page=0)
    
    with pytest.raises(ValidationError, match="Page size must be between 1 and 100"):
        await document_service.get_documents(test_db, page_size=101)

@pytest.mark.asyncio
async def test_document_generation(document_service):
    """Test document content generation"""
    result = await document_service.generate_document_content(
        name="Test User",
        date="2024-01-01",
        amount=100.50,
        template_type="receipt"
    )
    
    assert result["doc_id"] == "mock-doc-id"
    assert result["doc_url"] == "https://docs.google.com/document/d/mock-doc-id/edit"
    assert "content" in result
    assert result["name"] == "Test User"
    assert result["date"] == "2024-01-01"
    assert result["amount"] == 100.50