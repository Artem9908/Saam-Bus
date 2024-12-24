import pytest
from app.services.google_drive import GoogleDriveService
from app.exceptions import GoogleAPIError

@pytest.mark.asyncio
async def test_google_drive_upload():
    service = GoogleDriveService()
    test_content = "Test document content"
    test_filename = "test_doc.txt"
    
    result = await service.upload_document(test_content, test_filename)
    
    assert result["doc_id"] is not None
    assert result["doc_url"] is not None
    assert "drive.google.com" in result["doc_url"] 