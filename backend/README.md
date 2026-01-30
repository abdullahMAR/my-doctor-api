# My Doctor API - Backend Server

This is the backend API for the My Doctor application, built with FastAPI and SQLite.

## Requirements

- Python 3.8+
- FastAPI
- SQLite

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

This backend is ready to deploy on Render.com:
1. Push to GitHub
2. Connect to Render
3. Select "Web Service"
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
