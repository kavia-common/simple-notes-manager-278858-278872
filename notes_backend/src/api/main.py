from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.core.logging_config import configure_logging
from src.core.routers.notes import router as notes_router

# Configure application-level logging early
configure_logging()

# FastAPI application metadata with OpenAPI tags
app = FastAPI(
    title="Notes API",
    version="1.0.0",
    description="A simple, secure Notes API providing in-memory CRUD operations with a layered architecture."
)

# OpenAPI tag definitions for grouping endpoints
openapi_tags = [
    {
        "name": "Health",
        "description": "Service health and diagnostics."
    },
    {
        "name": "Notes",
        "description": "CRUD operations for notes."
    },
]
app.openapi_tags = openapi_tags  # type: ignore[attr-defined]

# CORS configuration per requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health Check", description="Simple health check endpoint.")
def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"message": "Healthy"})

# Include Notes router
app.include_router(notes_router, prefix="", tags=["Notes"])
