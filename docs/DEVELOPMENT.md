# Development Guide

## Setup

1. Clone the repository
2. Copy environment file:
   ```bash
   cp .env.example .env
   ```

# Add to setup section

## Credentials Setup

1. Place Google credentials file in the `credentials/` directory:
   ```bash
   cp path/to/your/credentials.json credentials/
   ```

2. Update `.env` file with the correct path:
   ```
   GOOGLE_CREDENTIALS_PATH=/app/credentials/your-credentials-file.json
   ```

3. Install dependencies:
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```

4. Start services:
   ```bash
   docker-compose up -d
   ```

## Development Scripts

- `scripts/cleanup.sh` - Clean build artifacts and cache
- `scripts/backend-tests.sh` - Run backend tests
- `scripts/db-migrate.sh` - Run database migrations
- `scripts/deploy.sh` - Deploy application
- `scripts/wait-for-it.sh` - Wait for service availability