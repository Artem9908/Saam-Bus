#!/bin/bash

# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# Remove test database
rm -f backend/test.db

# Remove virtual environments
rm -rf backend/venv
rm -rf backend/env

# Remove pytest cache
rm -rf .pytest_cache
rm -rf backend/.pytest_cache

# Remove duplicate directories
rm -rf backend/backend

# Remove node modules (if needed)
# rm -rf frontend/node_modules

echo "Cleanup completed!" 