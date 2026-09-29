from __future__ import annotations

import secrets
from typing import Any
from fastapi import Depends, Header, HTTPException, status

from core.config import ADMIN_KEY
from repositories.dataset_repository import read_dataset
from repositories.session_repository import SESSIONS


def get_current_session(
    authorization: str | None = Header(default=None),
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Standard reusable session dependency.
    Validates Bearer token format, SQLite-backed session validity and expiration,
    and returns the authenticated (user_record, profile) tuple.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
        )
    token = authorization.split(" ", 1)[1].strip()
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


def get_optional_session(
    authorization: str | None = Header(default=None),
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Returns the authenticated session tuple if a valid bearer token is provided, else None."""
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    try:
        return get_current_session(authorization)
    except HTTPException:
        return None


def get_current_user(
    session: tuple[dict[str, Any], dict[str, Any]] = Depends(get_current_session),
) -> dict[str, Any]:
    """Dependency that returns the authoritative user_record for the authenticated user."""
    return session[0]


def verify_admin_key(x_admin_key: str | None = Header(default=None)) -> bool:
    """Strictly validates the administrative API key using constant-time comparison."""
    if not x_admin_key or not secrets.compare_digest(x_admin_key, ADMIN_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin API key.",
        )
    return True


def verify_resource_ownership(
    target_user_id: str,
    session: tuple[dict[str, Any], dict[str, Any]],
    admin_key_candidate: str | None = None,
) -> bool:
    """
    Enforces resource ownership.
    Ensures a logged-in user can never access or modify another user's private resources
    unless valid administrative credentials are provided.
    """
    if admin_key_candidate and secrets.compare_digest(admin_key_candidate, ADMIN_KEY):
        return True

    current_record, _ = session
    if current_record.get("id") == target_user_id:
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden: You do not have permission to access another user's private resources.",
    )
