from __future__ import annotations

import threading
from typing import Dict, List, Optional

from src.core.models import Note, NoteCreate, NoteUpdate


class RepositoryError(Exception):
    """Generic repository error to avoid leaking internal details."""
    pass


# PUBLIC_INTERFACE
class InMemoryNotesRepository:
    """Thread-safe in-memory repository for storing notes."""

    def __init__(self) -> None:
        """Create an in-memory notes repository."""
        self._lock = threading.Lock()
        self._notes: Dict[int, Note] = {}
        self._next_id: int = 1

    def list_notes(self) -> List[Note]:
        """Return all notes."""
        with self._lock:
            return list(self._notes.values())

    def create_note(self, payload: NoteCreate) -> Note:
        """Create a new note with an auto-incremented ID."""
        with self._lock:
            note_id = self._next_id
            self._next_id += 1
            note = Note(id=note_id, title=payload.title, content=payload.content or "")
            self._notes[note_id] = note
            return note

    def get_note(self, note_id: int) -> Optional[Note]:
        """Retrieve a note by ID, or None if not found."""
        with self._lock:
            return self._notes.get(note_id)

    def update_note(self, note_id: int, payload: NoteUpdate) -> Optional[Note]:
        """Update an existing note by ID. Returns updated note or None if not found."""
        with self._lock:
            existing = self._notes.get(note_id)
            if existing is None:
                return None
            updated = existing.model_copy()
            if payload.title is not None:
                updated.title = payload.title
            if payload.content is not None:
                updated.content = payload.content
            self._notes[note_id] = updated
            return updated

    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID. Returns True if deleted, False if not found."""
        with self._lock:
            return self._notes.pop(note_id, None) is not None
