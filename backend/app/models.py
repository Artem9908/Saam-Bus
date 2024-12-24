from sqlalchemy import Column, Integer, String, Date, Float, Text, DateTime, text
from datetime import datetime
from .database import Base

class GeneratedDocument(Base):
    __tablename__ = "generated_documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    template_type = Column(String, nullable=True)
    doc_id = Column(String, nullable=True)
    doc_url = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    google_doc_id = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime("%Y-%m-%d"),
            "amount": self.amount,
            "doc_id": self.doc_id,
            "doc_url": self.doc_url,
            "content": self.content,
            "google_doc_id": self.google_doc_id,
            "created_at": self.created_at.isoformat()
        }