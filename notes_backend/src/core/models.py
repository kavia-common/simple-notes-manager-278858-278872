from typing import Optional
from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base fields for a note used across create and update operations."""

    title: str = Field(..., min_length=1, max_length=120, description="Title of the note (1..120 characters).")
    content: Optional[str] = Field(default="", max_length=5000, description="Content/body of the note (0..5000 characters).")


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Payload model for creating a note."""
    pass


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Payload model for updating a note."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=120, description="Updated title (1..120 characters).")
    content: Optional[str] = Field(default=None, max_length=5000, description="Updated content (0..5000 characters).")


# PUBLIC_INTERFACE
class Note(BaseModel):
    """Representation of a note entity returned by the API."""

    id: int = Field(..., description="Unique identifier of the note.")
    title: str = Field(..., min_length=1, max_length=120, description="Title of the note (1..120 characters).")
    content: Optional[str] = Field(default="", max_length=5000, description="Content/body of the note (0..5000 characters).")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Shopping List",
                "content": "Milk, Eggs, Bread",
            }
        }
