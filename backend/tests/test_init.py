from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from app.database import Base
from app.main import app
from fastapi import FastAPI

def test_module_exports():
    """Test that all expected objects are exported"""
    # Test that Base exists and is a class
    assert isinstance(Base, type)
    
    # Test that Base is a SQLAlchemy declarative base
    assert hasattr(Base, 'metadata')
    assert hasattr(Base, 'registry')
    
    # Test that Base can be used to create models
    class TestModel(Base):
        __tablename__ = 'test'
        id = Column(Integer, primary_key=True)
        name = Column(String)
    
    # Test that the model was created correctly
    assert hasattr(TestModel, '__table__')
    assert TestModel.__tablename__ == 'test'
    assert hasattr(TestModel, 'id')
    assert TestModel.id.primary_key
    
    # Test FastAPI app
    assert isinstance(app, FastAPI)