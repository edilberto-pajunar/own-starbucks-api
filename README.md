# Starbucks Backend API

A FastAPI-based backend for a Starbucks ordering system.

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Available Endpoints

### Root

- `GET /` - Welcome message

### Drinks

- `GET /api/v1/drinks/` - Get all drinks
- `GET /api/v1/drinks/customized` - Get customized drinks

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── models/           # Pydantic models
│   ├── routers/          # API route handlers
│   │   └── v1/
│   │       └── drinks.py # Drinks endpoints
│   └── schemas/          # Data schemas
├── venv/                 # Virtual environment
└── README.md
```

## Development

To add new routes:

1. Create router in `app/routers/v1/`
2. Register router in `app/main.py`
3. Define models in `app/models/`
