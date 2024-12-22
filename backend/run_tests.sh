#!/bin/sh

# Set environment variables for testing
export TESTING=true
export DATABASE_URL="sqlite:///:memory:"
export REDIS_HOST="localhost"
export REDIS_PORT=6379
export PYTHONPATH=/app

# Run tests
pytest -v --cov=app --cov-report=term-missing tests/