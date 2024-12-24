from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from .database import get_db, engine
from .services.document import DocumentService
from .services.google_drive import GoogleDriveService
from .exceptions import ValidationError, DocumentServiceException, TemplateError, GoogleAPIError
from .models import GeneratedDocument
import logging
from fastapi.middleware.cors import CORSMiddleware
from .utils.logger import logger

logger = logging.getLogger(__name__)

def get_document_service():
    return DocumentService()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentRequest(BaseModel):
    name: str = Field(
        ..., 
        min_length=2,
        error_messages={
            "min_length": "Name must be at least 2 characters long"
        }
    )
    date: str
    amount: float = Field(
        ...,
        gt=0,
        le=1000000,
        error_messages={
            "gt": "Amount must be greater than 0",
            "le": "Amount cannot exceed 1,000,000"
        }
    )
    template_type: Optional[str] = "receipt"

    @validator("date")
    def check_date_not_future(cls, value):
        parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
        if parsed_date > datetime.today().date():
            raise ValueError("Date cannot be in the future")
        return value

@app.get("/", tags=["Health"])
def health_check():
    """
    Health-check route.
    """
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/generate-document", tags=["Documents"])
async def generate_document(
    request: DocumentRequest,
    db: Session = Depends(get_db),
    service: DocumentService = Depends(get_document_service)
):
    try:
        # Generate document content
        result = await service.generate_document_content(
            name=request.name,
            date=request.date,
            amount=request.amount,
            template_type=request.template_type
        )
        
        # Create database record
        document = GeneratedDocument(
            name=request.name,
            date=datetime.strptime(request.date, "%Y-%m-%d").date(),
            amount=request.amount,
            content=result["content"],
            doc_id=result.get("doc_id"),
            doc_url=result.get("doc_url")
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return {
            "status": "success",
            "data": document,
            "message": "Document generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents", tags=["Documents"])
async def get_documents(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """Get paginated documents"""
    service = DocumentService()
    try:
        result = await service.get_documents(db, page=page, page_size=page_size)
        # The items are already GeneratedDocument objects, so we need to convert them to dicts
        return {
            "data": {
                "items": [item.to_dict() for item in result["items"]],
                "total": result["total"],
                "page": result["page"],
                "page_size": result["page_size"],
                "pages": result["pages"]
            }
        }
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except DocumentServiceException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/{doc_id}", tags=["Documents"])
async def get_document(
    doc_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific document by ID"""
    try:
        document = db.query(GeneratedDocument).filter(
            GeneratedDocument.doc_id == doc_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
            
        return {
            "data": document.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/{doc_id}/save-to-google", tags=["Documents"])
async def save_to_google_drive(
    doc_id: str,
    db: Session = Depends(get_db),
    service: GoogleDriveService = Depends(lambda: GoogleDriveService())
):
    """Save a document to Google Drive"""
    try:
        # Get document from database
        document = db.query(GeneratedDocument).filter(
            GeneratedDocument.doc_id == doc_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Generate filename
        filename = f"{document.name}_{document.date.strftime('%Y%m%d')}.txt"
        
        # Upload to Google Drive
        result = await service.upload_document(
            content=document.content,
            filename=filename
        )
        
        # Update document with Google Drive info
        document.google_doc_id = result['doc_id']
        document.doc_url = result['doc_url']
        db.commit()
        
        return {
            "status": "success",
            "data": {
                "google_doc_id": result['doc_id'],
                "doc_url": result['doc_url']
            }
        }
    except GoogleAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save to Google Drive: {str(e)}")