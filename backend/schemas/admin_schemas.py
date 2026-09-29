from __future__ import annotations

from typing import Any
from pydantic import BaseModel


class AdminUserPatch(BaseModel):
    data: dict[str, Any]


class AdminDatasetUpdate(BaseModel):
    data: dict[str, Any]


class EnrollRequest(BaseModel):
    course_id: str
