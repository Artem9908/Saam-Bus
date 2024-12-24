from datetime import date, datetime
import pytest
from app import models

@pytest.mark.asyncio
async def test_health_check(async_client):
    """Test the health check endpoint"""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

@pytest.mark.asyncio
async def test_generate_document(async_client):
    """Test document generation"""
    test_data = {
        "name": "Test User",
        "date": str(date.today()),
        "amount": 100.50,
        "template_type": "receipt"
    }
    
    response = await async_client.post("/generate-document", json=test_data)
    assert response.status_code == 200
    
    data = response.json()["data"]
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["name"] == test_data["name"]
    assert float(data["amount"]) == test_data["amount"]
    assert "content" in data
    assert "doc_id" in data
    assert "doc_url" in data

@pytest.mark.asyncio
async def test_generate_contract_document(async_client):
    """Test contract document generation"""
    test_data = {
        "name": "Test Client",
        "date": str(date.today()),
        "amount": 1000.50,
        "template_type": "contract"
    }
    
    response = await async_client.post("/generate-document", json=test_data)
    assert response.status_code == 200
    
    data = response.json()["data"]
    assert data["name"] == test_data["name"]
    assert float(data["amount"]) == test_data["amount"]
    assert "CONTRACT" in data["content"]
    assert "Test Client" in data["content"]
    assert str(date.today()) in data["content"]

@pytest.mark.asyncio
async def test_get_documents_pagination(async_client, test_db):
    """Test documents endpoint pagination"""
    # Create 15 test documents
    for i in range(15):
        doc = models.GeneratedDocument(
            name=f"Test User {i}",
            date=datetime.now().date(),
            amount=100.50 + i,
            content=f"Test content {i}",
            doc_id=f"mock-{i}",
            template_type="receipt"
        )
        test_db.add(doc)
    test_db.commit()

    # Test default pagination (page 1, size 10)
    response = await async_client.get("/documents")
    assert response.status_code == 200
    data = response.json()["data"]
    
    # Verify pagination data
    assert len(data["items"]) == 10  # First page should have 10 items
    assert data["total"] == 15       # Total number of documents
    assert data["page"] == 1         # Current page
    assert data["page_size"] == 10   # Items per page
    assert data["pages"] == 2        # Total number of pages (15 items / 10 per page = 2 pages)

    # Test second page
    response = await async_client.get("/documents?page=2")
    assert response.status_code == 200
    data = response.json()["data"]
    
    # Verify second page data
    assert len(data["items"]) == 5   # Second page should have remaining 5 items
    assert data["total"] == 15
    assert data["page"] == 2
    assert data["page_size"] == 10
    assert data["pages"] == 2

    # Test custom page size
    response = await async_client.get("/documents?page_size=5")
    assert response.status_code == 200
    data = response.json()["data"]
    
    # Verify custom page size
    assert len(data["items"]) == 5   # Should return exactly 5 items
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert data["pages"] == 3        # 15 items / 5 per page = 3 pages

@pytest.mark.asyncio
async def test_generate_documents_with_templates(async_client):
    """Test document generation with different templates"""
    templates = ['receipt', 'invoice', 'contract']
    
    for template_type in templates:
        test_data = {
            "name": "Test User",
            "date": str(date.today()),
            "amount": 100.50,
            "template_type": template_type
        }
        
        response = await async_client.post("/generate-document", json=test_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        assert data["name"] == test_data["name"]
        assert float(data["amount"]) == test_data["amount"]
        assert template_type.upper() in data["content"]

@pytest.mark.asyncio
async def test_generate_document_invalid_template(async_client):
    """Test document generation with invalid template"""
    test_data = {
        "name": "Test User",
        "date": str(date.today()),
        "amount": 100.50,
        "template_type": "invalid"
    }
    
    response = await async_client.post("/generate-document", json=test_data)
    assert response.status_code == 422
    assert "Invalid template type" in response.json()["detail"]

@pytest.mark.asyncio
async def test_generate_document_validation_error(async_client):
    """Test document generation with invalid data"""
    test_data = {
        "name": "A",  # Too short
        "date": str(date.today()),
        "amount": 100.50,
        "template_type": "receipt"
    }
    
    response = await async_client.post("/generate-document", json=test_data)
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("String should have at least 2 characters" in e["msg"] 
              for e in error_detail)

# ... rest of the file remains the same ... 