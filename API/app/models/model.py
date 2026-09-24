"""Pydantic schemas for players."""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, field_serializer

class PlayerSchema(BaseModel):
    id: int
    name: str
    number: Optional[int] = None
    position: Optional[str] = None
    # image_url: Optional[str] = None
    citizenship: Optional[List[str]] = None
    # citizenship_flag_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    height: Optional[int] = None
    weight: Optional[int] = None

    @field_serializer("citizenship")
    def serialize_citizenship(self, value: Optional[List[str]]) -> Optional[str]:
        if value is None:
            return None
        return ", ".join(value)
