from datetime import datetime
from app.models import GeneratedDocument

def test_document_creation(test_db):
    """Test creating a document in the database"""
    doc = GeneratedDocument(
        name="Test User",
        date=datetime.now().date(),
        amount=100.50,
        content="Test content"
    )
    
    test_db.add(doc)
    test_db.commit()
    
    assert doc.id is not None
    assert doc.name == "Test User"
    assert doc.amount == 100.50

def test_document_to_dict(sample_document):
    """Test the to_dict method of GeneratedDocument"""
    doc_dict = sample_document.to_dict()
    
    assert isinstance(doc_dict, dict)
    assert doc_dict["name"] == sample_document.name
    assert float(doc_dict["amount"]) == sample_document.amount
    assert "created_at" in doc_dict 