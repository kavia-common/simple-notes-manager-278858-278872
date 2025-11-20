from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import Response

from src.core.models import Note, NoteCreate, NoteUpdate
from src.core.service import NotesService, NotFoundError
from src.api.main import get_notes_service

logger = logging.getLogger(__name__)

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "/notes",
    response_model=List[Note],
    status_code=status.HTTP_200_OK,
    summary="List notes",
    description="Returns the list of all notes. Initially returns an empty list.",
)
def list_notes(service: NotesService = Depends(get_notes_service)) -> List[Note]:
    """List all notes.

    Returns:
        List[Note]: All notes currently stored.
    """
    try:
        return service.list_notes()
    except Exception:
        # Avoid leaking internals
        logger.exception("Unhandled error while listing notes")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


# PUBLIC_INTERFACE
@router.post(
    "/notes",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create note",
    description="Create a new note with a title and optional content.",
)
def create_note(payload: NoteCreate, service: NotesService = Depends(get_notes_service)) -> Note:
    """Create a note.

    Args:
        payload: The note data to create.

    Returns:
        Note: The created note with its ID.
    """
    try:
        return service.create_note(payload)
    except Exception:
        logger.exception("Unhandled error while creating note")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


# PUBLIC_INTERFACE
@router.get(
    "/notes/{note_id}",
    response_model=Note,
    status_code=status.HTTP_200_OK,
    summary="Get note",
    description="Retrieve a note by its ID.",
)
def get_note(
    note_id: int = Path(..., ge=1, description="ID of the note to retrieve"),
    service: NotesService = Depends(get_notes_service),
) -> Note:
    """Get a note by ID.

    Args:
        note_id: ID of the note to retrieve.

    Returns:
        Note: The requested note.

    Raises:
        HTTPException: 404 if not found; 500 for unexpected errors.
    """
    try:
        return service.get_note(note_id)
    except NotFoundError:
        logger.info("Note %s not found", note_id)
        raise HTTPException(status_code=404, detail="Note not found")  # noqa: B904
    except Exception:
        logger.exception("Unhandled error while retrieving note %s", note_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


# PUBLIC_INTERFACE
@router.put(
    "/notes/{note_id}",
    response_model=Note,
    status_code=status.HTTP_200_OK,
    summary="Update note",
    description="Update an existing note by its ID.",
)
def update_note(
    payload: NoteUpdate,
    note_id: int = Path(..., ge=1, description="ID of the note to update"),
    service: NotesService = Depends(get_notes_service),
) -> Note:
    """Update a note by ID.

    Args:
        payload: Fields to update.
        note_id: ID of the note to update.

    Returns:
        Note: The updated note.

    Raises:
        HTTPException: 404 if not found; 500 for unexpected errors.
    """
    try:
        return service.update_note(note_id, payload)
    except NotFoundError:
        logger.info("Note %s not found for update", note_id)
        raise HTTPException(status_code=404, detail="Note not found")  # noqa: B904
    except Exception:
        logger.exception("Unhandled error while updating note %s", note_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


# PUBLIC_INTERFACE
@router.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete note",
    description="Delete a note by its ID.",
)
def delete_note(
    note_id: int = Path(..., ge=1, description="ID of the note to delete"),
    service: NotesService = Depends(get_notes_service),
) -> Response:
    """Delete a note by ID.

    Args:
        note_id: ID of the note to delete.

    Returns:
        Response: 204 No Content on success.

    Raises:
        HTTPException: 404 if not found; 500 for unexpected errors.
    """
    try:
        service.delete_note(note_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotFoundError:
        logger.info("Note %s not found for deletion", note_id)
        raise HTTPException(status_code=404, detail="Note not found")  # noqa: B904
    except Exception:
        logger.exception("Unhandled error while deleting note %s", note_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
