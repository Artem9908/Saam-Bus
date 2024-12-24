import pytest
from httpx import AsyncClient
from datetime import datetime

@pytest.mark.integration
async def test_complete_document_flow(async_client: AsyncClient, test_db):
    # Create document
    doc_data = {
        "name": "Integration Test",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": 150.75,
        "template_type": "receipt"
    }
    
    response = await async_client.post("/generate-document", json=doc_data)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["doc_id"] == "mock-doc-id"
    
    # Verify document in database
    response = await async_client.get(f"/documents/{data['doc_id']}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == doc_data["name"]
    
    # Test document listing with filters
    response = await async_client.get(
        "/documents",
        params={"name": "Integration"}
    )
    assert response.status_code == 200
    assert len(response.json()["data"]["items"]) == 1 