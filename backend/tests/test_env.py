import os
import sys
from pathlib import Path

# Set testing environment variables before any imports
os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_DB"] = "0"
os.environ["SKIP_GOOGLE_AUTH"] = "true"

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# Now we can safely import and check
from app.config import TESTING
assert TESTING is True, "TESTING environment variable not properly set"