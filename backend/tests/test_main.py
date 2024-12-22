from datetime import date, datetime
import pytest

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
        "amount": 100.50
    }
    
    response = await async_client.post("/generate-document", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == test_data["name"]
    assert float(data["amount"]) == test_data["amount"]

# ... rest of the file remains the same ... 