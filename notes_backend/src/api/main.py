from __future__ import annotations

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.core.logging_config import configure_logging
from src.core.repository import InMemoryNotesRepository
from src.core.routers.notes import router as notes_router
from src.core.service import NotesService

# Initialize module logger
logger = logging.getLogger(__name__)

# Configure application-level logging early
configure_logging()

# FastAPI application metadata with OpenAPI tags
app = FastAPI(
    title="Notes API",
    version="1.0.0",
    description="A simple, secure Notes API providing in-memory CRUD operations with a layered architecture.",
    openapi_tags=[
        {"name": "Health", "description": "Service health and diagnostics."},
        {"name": "Notes", "description": "CRUD operations for notes."},
    ],
)

# CORS configuration per requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


def _init_services() -> None:
    """Initialize and attach repository/service singletons to app.state.

    This avoids uncontrolled module-level globals and ties lifecycle to the app.
    """
    # Only initialize once per process/app instance
    if not hasattr(app.state, "notes_repo"):
        app.state.notes_repo = InMemoryNotesRepository()
        logger.info("Initialized InMemoryNotesRepository")
    if not hasattr(app.state, "notes_service"):
        app.state.notes_service = NotesService(app.state.notes_repo)
        logger.info("Initialized NotesService")


@app.on_event("startup")
def on_startup() -> None:
    """FastAPI startup hook to initialize app-scoped services."""
    _init_services()
    logger.info("Application startup complete")


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Simple health check endpoint.",
)
def health_check() -> JSONResponse:
    """Health check endpoint.

    Returns:
        JSONResponse: A simple message indicating service health.
    """
    return JSONResponse({"message": "Healthy"})


# Include Notes router; router resolves its own dependency from app.state
app.include_router(notes_router, prefix="", tags=["Notes"], dependencies=[])
