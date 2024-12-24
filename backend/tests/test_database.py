import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from app.database import Base, get_db, init_db, SessionLocal
from app.config import TESTING

def test_init_db(test_db):
    """Test database initialization"""
    # Tables should be created
    inspector = inspect(test_db.get_bind())
    tables = inspector.get_table_names()
    assert "generated_documents" in tables

def test_get_db():
    """Test database session management"""
    db_generator = get_db()
    db: Session = next(db_generator)
    
    try:
        # Check that we got a valid session
        assert isinstance(db, Session)
        assert db.is_active
    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass

def test_testing_engine():
    """Test database engine configuration in test environment"""
    from app.database import SessionLocal
    
    # Get engine from session
    engine = SessionLocal().get_bind()
    
    # Check that we're using SQLite for testing
    assert engine.dialect.name == "sqlite"
    # Check that we're using in-memory database
    assert str(engine.url).startswith("sqlite:///:memory:")

def test_db_session_cleanup():
    """Test that database sessions are properly cleaned up"""
    db_generator = get_db()
    db: Session = next(db_generator)
    
    # Session should be active initially
    assert db.is_active
    
    try:
        next(db_generator)
    except StopIteration:
        pass
    
    # Test that session is closed by trying to execute a query
    with pytest.raises(Exception):
        db.execute("SELECT 1")