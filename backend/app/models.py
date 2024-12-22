from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Index
from sqlalchemy.sql import func
from .database import Base

class GeneratedDocument(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    date = Column(Date, index=True)
    amount = Column(Float)
    content = Column(String)
    doc_url = Column(String, nullable=True)
    doc_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Create indexes
    __table_args__ = (
        Index('idx_name', name),
        Index('idx_date', date),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": str(self.date),
            "amount": self.amount,
            "content": self.content,
            "doc_url": self.doc_url,
            "doc_id": self.doc_id,
            "created_at": str(self.created_at)
        }