from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models import GeneratedDocument
from .google_docs import GoogleDocsService
from typing import Optional, Dict
from ..config import SKIP_GOOGLE_AUTH

class DocumentService:
    def __init__(self):
        self.google_docs = GoogleDocsService()

    def generate_document_content(self, name: str, date: str, amount: float) -> Dict[str, str]:
        """Generate document content and create Google Doc."""
        content = f"""
        DOCUMENT RECEIPT
        
        Name: {name}
        Date: {date}
        Amount: ${amount:.2f}
        
        This document certifies that {name} has paid the amount of ${amount:.2f} on {date}.
        
        Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """

        if SKIP_GOOGLE_AUTH:
            return {
                "content": content,
                "doc_url": "http://localhost:8000/mock-doc",
                "doc_id": "mock-id-123"
            }

        doc_id = self.google_docs.create_document(
            f"Receipt for {name} - {date}",
            content
        )
        
        return {
            "content": content,
            "doc_url": f"https://docs.google.com/document/d/{doc_id}" if doc_id else None,
            "doc_id": doc_id
        }

    async def get_documents(self, db: Session, name: Optional[str] = None, date: Optional[str] = None):
        """Get list of documents with optional filters"""
        query = db.query(GeneratedDocument)
        
        if name:
            query = query.filter(GeneratedDocument.name.ilike(f"%{name}%"))
        
        if date:
            try:
                filter_date = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(GeneratedDocument.date == filter_date)
            except ValueError:
                pass
        
        # Выполняем запрос и преобразуем результаты
        documents = query.all()
        return [doc.to_dict() for doc in documents] 