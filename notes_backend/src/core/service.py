from __future__ import annotations

import logging
from typing import List

from src.core.models import Note, NoteCreate, NoteUpdate
from src.core.repository import InMemoryNotesRepository

logger = logging.getLogger(__name__)


class NotFoundError(Exception):
    """Raised when an entity is not found."""
    pass


def _sanitize_text(text: str) -> str:
    """Trim whitespace and normalize input to prevent accidental leading/trailing spaces."""
    return text.strip()


# PUBLIC_INTERFACE
class NotesService:
    """Service layer for notes, encapsulating business rules and validation."""

    def __init__(self, repository: InMemoryNotesRepository) -> None:
        self._repo = repository

    def list_notes(self) -> List[Note]:
        try:
            return self._repo.list_notes()
        except Exception as exc:
            logger.error("Failed to list notes: %s", str(exc))
            raise

    def create_note(self, payload: NoteCreate) -> Note:
        try:
            cleaned = NoteCreate(
                title=_sanitize_text(payload.title),
                content=_sanitize_text(payload.content or ""),
            )
            return self._repo.create_note(cleaned)
        except Exception as exc:
            logger.error("Failed to create note: %s", str(exc))
            raise

    def get_note(self, note_id: int) -> Note:
        try:
            note = self._repo.get_note(note_id)
            if note is None:
                raise NotFoundError("Note not found")
            return note
        except NotFoundError:
            raise
        except Exception as exc:
            logger.error("Failed to get note %s: %s", note_id, str(exc))
            raise

    def update_note(self, note_id: int, payload: NoteUpdate) -> Note:
        try:
            cleaned = NoteUpdate(
                title=_sanitize_text(payload.title) if payload.title is not None else None,
                content=_sanitize_text(payload.content) if payload.content is not None else None,
            )
            updated = self._repo.update_note(note_id, cleaned)
            if updated is None:
                raise NotFoundError("Note not found")
            return updated
        except NotFoundError:
            raise
        except Exception as exc:
            logger.error("Failed to update note %s: %s", note_id, str(exc))
            raise

    def delete_note(self, note_id: int) -> None:
        try:
            deleted = self._repo.delete_note(note_id)
            if not deleted:
                raise NotFoundError("Note not found")
        except NotFoundError:
            raise
        except Exception as exc:
            logger.error("Failed to delete note %s: %s", note_id, str(exc))
            raise
