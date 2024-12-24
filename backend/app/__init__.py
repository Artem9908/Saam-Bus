from .utils.logger import setup_logger
setup_logger()  # Initialize logging first

from .database import Base, get_db, init_db
from .main import app

__all__ = ['app', 'Base', 'get_db', 'init_db']