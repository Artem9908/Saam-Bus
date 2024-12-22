from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models
from .database import get_db
from .services.document import DocumentService
from datetime import datetime
from typing import List, Optional
from .services.cache import cache_response
from pydantic import BaseModel
from .config import CORS_ORIGINS
import logging

logger = logging.getLogger(__name__)

class DocumentRequest(BaseModel):
    name: str
    date: str
    amount: float

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_service = DocumentService()

@app.get("/")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/generate-document")
def generate_document(
    request: DocumentRequest = Body(...),
    db: Session = Depends(get_db)
):
    try:
        doc_data = document_service.generate_document_content(
            request.name, 
            request.date, 
            request.amount
        )
        
        doc = models.GeneratedDocument(
            name=request.name,
            date=datetime.strptime(request.date, "%Y-%m-%d").date(),
            amount=request.amount,
            content=doc_data["content"],
            doc_url=doc_data["doc_url"],
            doc_id=doc_data["doc_id"]
        )
        
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc.to_dict()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
@cache_response(expire_time=300)
async def get_documents_endpoint(
    name: Optional[str] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        documents = await document_service.get_documents(db, name, date)
        return documents
    except Exception as e:
        logger.error(f"Error getting documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting documents: {str(e)}"
        )