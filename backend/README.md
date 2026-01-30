# My Doctor API - Backend Server

This is the backend API for the My Doctor application, built with FastAPI and supports both SQLite (local development) and PostgreSQL (production).

## Requirements

- Python 3.8+
- FastAPI
- SQLite (local development) or PostgreSQL (production)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

### Local Development (SQLite)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production or Testing with PostgreSQL
```bash
# Set your PostgreSQL connection string
set DATABASE_URL=postgresql://username:password@hostname:port/database

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

### 🚀 Deploy to Render (Free!)

See the comprehensive [**DEPLOYMENT_GUIDE.md**](./DEPLOYMENT_GUIDE.md) for detailed Arabic instructions on deploying to Render with free PostgreSQL database.

**Quick steps:**
1. Create PostgreSQL database on Render
2. Push code to GitHub
3. Create Web Service on Render
4. Set `DATABASE_URL` environment variable
5. Deploy! 🎉

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (optional, uses SQLite if not set)
  - Example: `postgresql://user:pass@host:5432/dbname`

