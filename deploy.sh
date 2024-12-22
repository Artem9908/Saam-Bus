#!/bin/bash

# Stop all running containers
docker-compose down

# Pull latest changes
git pull origin main

# Build and start containers
docker-compose up --build -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Show logs
docker-compose logs -f 