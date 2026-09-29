from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=1)


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)
    password: str = Field(min_length=6)
    role: str = "Statistical Investigator"
    department: str = "MoSPI"
    projectId: str = "SIH26101"
    account_type: str = "officer"


class UserUpdateRequest(BaseModel):
    name: str | None = None
