from __future__ import annotations

import secrets
from typing import Any
from fastapi import Header, HTTPException, status

from core.config import ADMIN_KEY
from repositories.dataset_repository import read_dataset
from services.auth_service import SESSIONS


def get_current_session(authorization: str | None = Header(default=None)) -> tuple[dict[str, Any], dict[str, Any]]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
        )
    token = authorization.split("Bearer ", 1)[1].strip()
    session = SESSIONS.get(token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session.",
        )

    dataset = read_dataset()
    for record in dataset.get("users", []):
        if record.get("id") == session["id"]:
            return record, session.get("profile") or record.get("profile") or {}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Session user no longer exists.",
    )


def verify_admin_key(x_admin_key: str | None = Header(default=None)) -> bool:
    if not x_admin_key or not secrets.compare_digest(x_admin_key, ADMIN_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin API key.",
        )
    return True
