#!/bin/bash

echo "Starting cleanup..."

# Clean Python cache files
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# Clean test artifacts
rm -f backend/test.db
rm -rf .pytest_cache
rm -rf backend/.pytest_cache
rm -rf frontend/coverage

# Clean build artifacts
rm -rf frontend/build
rm -rf backend/build
rm -rf backend/dist
rm -rf backend/*.egg-info

# Clean logs
rm -rf backend/logs/*
touch backend/logs/.gitkeep

echo "Cleanup completed!"