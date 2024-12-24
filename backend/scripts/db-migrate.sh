#!/bin/bash
set -e

echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U postgres; do
    echo "Database is unavailable - sleeping"
    sleep 1
done
echo "Database is ready!"

# Set Python path
export PYTHONPATH=$PYTHONPATH:/app

echo "Running database migrations..."
cd /app && alembic upgrade head
echo "Migrations completed!"

# Start the application
exec "$@"