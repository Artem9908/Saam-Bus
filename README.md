# Document Generation Service

A web application for generating and managing documents with Google Drive integration. Built with FastAPI, React, and PostgreSQL.

## Features

- 📄 Generate documents with custom data
- 📁 Store documents in Google Drive
- 📋 View document history
- 🔍 Filter documents by name and date
- ⚡ Redis caching for improved performance
- 🔒 Secure document storage
- 🌐 RESTful API
- 🐳 Docker containerization

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Redis (Caching)
- Alembic (Database migrations)
- pytest (Testing)

### Frontend
- React
- TailwindCSS
- React Router
- React Toastify

### Infrastructure
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Google Drive API

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js 18+
- Google Drive API credentials

## Installation

1. Clone the repository:

bash
git clone https://github.com/yourusername/document-generation-service.git
cd document-generation-service



2. Create environment files from examples:

bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env


3. Set up Google Drive API credentials:
   - Create a project in Google Cloud Console
   - Enable Google Drive API
   - Create service account credentials
   - Download credentials as `credentials.json`
   - Place `credentials.json` in the `backend/` directory

4. Start the application:

bash
docker-compose up --build


The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Backend Development

bash
cd backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload



### Frontend Development

bash
cd frontend
npm install
npm start


### Running Tests

Backend tests:

bash
cd backend
pytest -v


## API Documentation

The API documentation is available at `/docs` or `/redoc` when the backend is running.

Key endpoints:
- `POST /generate-document`: Generate a new document
- `GET /documents`: List all documents
- `GET /documents?name={name}&date={date}`: Filter documents

## Database Migrations

Create a new migration:

bash
cd backend
alembic revision -m "description"


Apply migrations:

bash
alembic upgrade head


## Project Structure

.
├── backend/ # FastAPI application
│ ├── app/
│ │ ├── services/ # Business logic
│ │ ├── models.py # Database models
│ │ └── main.py # FastAPI app
│ ├── tests/ # Python tests
│ └── alembic/ # Database migrations
├── frontend/ # React application
│ ├── src/
│ │ ├── components/ # React components
│ │ └── services/ # API services
│ └── public/
└── docker-compose.yml # Docker composition


## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a Pull Request

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `CORS_ORIGINS`: Allowed CORS origins
- `SKIP_GOOGLE_AUTH`: Skip Google authentication (for testing)

### Frontend
- `REACT_APP_API_URL`: Backend API URL

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.