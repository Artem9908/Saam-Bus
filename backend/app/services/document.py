from ..exceptions import ValidationError, GoogleAPIError, TemplateError, DatabaseError
from datetime import datetime
from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .google_docs import GoogleDocsService
from .templates import DocumentTemplate
from .cache import RedisCache
from .cache_decorator import cache_response
from ..models import GeneratedDocument
import logging
import os
from ..config import TESTING
from ..exceptions import DocumentServiceException


logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        self.google_docs = GoogleDocsService()
        self.cache = RedisCache()
        
    async def initialize(self):
        """Initialize service dependencies"""
        await self.cache.initialize()

    def validate_document_data(self, name: str, date: str, amount: float, template_type: str) -> None:
        """Validate all document input data"""
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long")
        
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
            if parsed_date > datetime.today().date():
                raise ValidationError("Date cannot be in the future")
        except ValueError:
            raise ValidationError("Invalid date format. Use YYYY-MM-DD")
        
        if amount <= 0:
            raise ValidationError("Amount must be greater than 0")
        if amount > 1000000:
            raise ValidationError("Amount cannot exceed 1,000,000")
        
        valid_templates = ["receipt", "invoice", "contract"]
        if template_type not in valid_templates:
            raise TemplateError(f"Invalid template type. Must be one of: {', '.join(valid_templates)}")

    def _get_cache_key(self, method_name: str, *args, **kwargs) -> str:
        """Generate a cache key from method name and arguments"""
        key_parts = [method_name]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        return ":".join(key_parts)

    @cache_response(expire_time=300)
    async def get_documents(self, db: Session, page: int = 1, page_size: int = 10, **filters) -> Dict:
        """Get paginated documents with caching"""
        # First ensure cache is initialized
        await self.initialize()
        # Validate parameters first, before any database operations
        if page < 1:
            raise ValidationError("Page number must be positive")
        if not 1 <= page_size <= 100:
            raise ValidationError("Page size must be between 1 and 100")
        
        try:
            query = db.query(GeneratedDocument)
            
            # Apply filters
            if filters.get('name'):
                query = query.filter(GeneratedDocument.name.ilike(f"%{filters['name']}%"))
            
            if filters.get('date'):
                try:
                    parsed_date = datetime.strptime(filters['date'], "%Y-%m-%d").date()
                    query = query.filter(GeneratedDocument.date == parsed_date)
                except ValueError:
                    raise ValidationError("Invalid date format. Use YYYY-MM-DD")
            
            # Get total count before pagination
            total_count = query.count()
            
            # Apply pagination
            query = query.order_by(GeneratedDocument.created_at.desc())
            query = query.offset((page - 1) * page_size).limit(page_size)
            
            documents = query.all()
            
            return {
                "items": documents,
                "total": total_count,
                "page": page,
                "page_size": page_size,
                "pages": (total_count + page_size - 1) // page_size
            }
            
        except ValidationError:
            raise  # Re-raise validation errors directly
        except Exception as e:
            logger.error(f"Database error while getting documents: {e}")
            raise DatabaseError(f"Error retrieving documents: {str(e)}")

    async def generate_document_content(self, name: str, date: str, amount: float, template_type: str) -> Dict:
        try:
            self.validate_document_data(name, date, amount, template_type)
            
            content = DocumentTemplate.generate_template(template_type, {
                "name": name,
                "date": date,
                "amount": amount
            })
            
            result = {
                "name": name,
                "date": date,
                "amount": amount,
                "content": content,
            }
            
            if not TESTING:
                try:
                    google_doc = await self.google_docs.create_document(
                        title=name,
                        content=content
                    )
                    result["doc_id"] = google_doc["doc_id"]
                    result["doc_url"] = google_doc["doc_url"]
                except Exception as e:
                    if isinstance(e, GoogleAPIError):
                        raise
                    raise GoogleAPIError(f"Failed to create Google document: {str(e)}")
            else:
                result["doc_id"] = "mock-doc-id"
                result["doc_url"] = "https://docs.google.com/document/d/mock-doc-id/edit"
            
            return result
        except (ValidationError, TemplateError, GoogleAPIError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error in document generation: {e}")
            raise DocumentServiceException(f"Failed to generate document: {str(e)}")