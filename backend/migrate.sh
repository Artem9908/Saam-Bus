#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

echo "Running database migrations..."
alembic upgrade head
echo "Migrations completed!"

# Start the application
exec "$@"