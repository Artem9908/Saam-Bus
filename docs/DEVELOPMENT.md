# Development Guide

## Setup

1. Clone the repository
2. Copy environment files:
   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

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
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
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
- `scripts/backend-tests.sh` - Run backend tests with coverage
- `scripts/db-migrate.sh` - Run database migrations
- `scripts/deploy.sh` - Deploy application
- `scripts/wait-for-it.sh` - Wait for service availability

## Testing

### Backend Tests
```bash
# Run all tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_document_service.py
```

### Frontend Tests
```bash
# Run all tests
cd frontend
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm test -- --watch
```

## Database Migrations

Create a new migration:
```bash
cd backend
alembic revision -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Code Style

### Backend
- Use `black` for Python code formatting
- Use `flake8` for linting
- Use `mypy` for type checking

### Frontend
- Use ESLint with TypeScript configuration
- Use Prettier for code formatting

## Debugging

### Backend
- Use FastAPI's automatic documentation at `/docs`
- Enable debug mode in `uvicorn` with `--reload --debug`

### Frontend
- Use React Developer Tools browser extension
- Use console.log with descriptive labels
```

3. The `docs/README.md` file looks good as is, but we should reference the new API documentation:


```106:113:docs/README.md
cd backend
pytest -v


## API Documentation

The API documentation is available at `/docs` or `/redoc` when the backend is running.

```


Replace with:
```markdown
## API Documentation

Detailed API documentation is available in [docs/API.md](./API.md).

The interactive API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
```

These updates provide more comprehensive documentation while maintaining consistency with the existing codebase and implementation details shown in the provided code snippets.