# Notes Backend (FastAPI)

A secure, Bandit-conscious FastAPI backend for a simple notes application. Implements a layered architecture (router → service → repository) with an in-memory data store.

## Features
- Endpoints:
  - GET /notes → List notes
  - POST /notes → Create note (201)
  - GET /notes/{id} → Retrieve note
  - PUT /notes/{id} → Update note
  - DELETE /notes/{id} → Delete note (204)
- Validation: title 1..120 chars, content 0..5000 chars. Input is trimmed in the service layer.
- CORS: allows http://localhost:3000 (methods GET, POST, PUT, DELETE; no credentials).
- Health check at `/`.

## Run locally
1. Create a venv and install dependencies:
   - python -m venv .venv
   - source .venv/bin/activate
   - pip install -r requirements.txt
2. Start the server:
   - uvicorn src.api.main:app --host 0.0.0.0 --port 3001

API Docs:
- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## Project structure
- src/api/main.py → FastAPI app, CORS, routing
- src/core/models.py → Pydantic models
- src/core/repository.py → Thread-safe in-memory repository
- src/core/service.py → Business logic and sanitization
- src/core/routers/notes.py → API endpoints (CRUD)
- src/core/logging_config.py → Structured logging configuration
- interfaces/openapi.json → Generated API spec snapshot

## Security and Compliance
- No secrets or sensitive data in code.
- Logging uses Python's logging library; no prints.
- Avoids insecure functions (eval/exec), unsafe YAML, and weak hashes.
- Errors return safe, generic messages; internal details are not exposed.
- All inputs validated and trimmed to prevent accidental whitespace issues.

## Limitations
- Data is stored in-memory and will be lost on server restart.
- This service does not include authentication; suitable for demo/local development.

## Regenerating OpenAPI
From the project root or container root:
- python -m src.api.generate_openapi
This writes the schema to `interfaces/openapi.json`.
