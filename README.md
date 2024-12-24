I'll help update the documentation files to ensure consistency and completeness. Let's review and update each one:

1. First, let's update the root `README.md` to be more comprehensive:

```markdown:README.md
# Document Generator Service

A web application for generating and managing documents with Google Drive integration.

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/document-generation-service.git
cd document-generation-service
```

2. Copy environment files:
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Set up Google Drive API credentials:
   - Place credentials file in `credentials/` directory
   - Update GOOGLE_CREDENTIALS_PATH in `.env`

4. Start the application:
```bash
docker-compose up --build
```

## Documentation

- [Development Guide](docs/DEVELOPMENT.md)
- [API Documentation](docs/API.md)
- [Full Documentation](docs/README.md)

## Available Services

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## License

MIT License - See [LICENSE](LICENSE) file for details.
```