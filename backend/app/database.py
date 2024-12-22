from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from .config import DATABASE_URL, TESTING

# Create declarative base instance
Base = declarative_base()

# Configure the engine
if TESTING:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    if TESTING:
        init_db()  # Ensure tables are created for tests
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
