import os

# Test configuration
TEST_DATABASE_URL = "sqlite:///:memory:"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["TESTING"] = "1" 