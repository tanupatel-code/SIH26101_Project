"""
StatSkill AI — Secure Password Hashing Service.
Supports bcrypt with standard-library PBKDF2-HMAC-SHA256 fallback.
Ensures passwords are never stored or logged in plaintext.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from typing import Any

# Try importing bcrypt, fallback to standard hashlib pbkdf2 if unavailable
try:
    import bcrypt
    _HAS_BCRYPT = True
except ImportError:
    _HAS_BCRYPT = False

# PBKDF2 parameters for fallback
_PBKDF2_ROUNDS = 120_000
_SALT_BYTES = 16


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt (or PBKDF2-HMAC-SHA256 fallback).
    Returns a formatted string suitable for storage.
    """
    if not password:
        raise ValueError("Password cannot be empty.")

    if _HAS_BCRYPT:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    # Fallback: pbkdf2_sha256$rounds$salt_hex$hash_hex
    salt_bytes = secrets.token_bytes(_SALT_BYTES)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt_bytes, _PBKDF2_ROUNDS
    )
    salt_hex = salt_bytes.hex()
    hash_hex = derived.hex()
    return f"pbkdf2_sha256${_PBKDF2_ROUNDS}${salt_hex}${hash_hex}"


def verify_password(plain_password: str, hashed_or_stored: str) -> bool:
    """
    Verifies a plaintext password against a hashed (or legacy demo plaintext) password.
    Uses constant-time comparison to prevent timing attacks.
    """
    if not plain_password or not hashed_or_stored:
        return False

    # Check if stored as bcrypt
    if hashed_or_stored.startswith("$2a$") or hashed_or_stored.startswith("$2b$"):
        if _HAS_BCRYPT:
            try:
                return bcrypt.checkpw(
                    plain_password.encode("utf-8"),
                    hashed_or_stored.encode("utf-8"),
                )
            except Exception:
                return False
        return False

    # Check if stored as PBKDF2
    if hashed_or_stored.startswith("pbkdf2_sha256$"):
        try:
            parts = hashed_or_stored.split("$")
            if len(parts) == 4:
                rounds = int(parts[1])
                salt_bytes = bytes.fromhex(parts[2])
                expected_hash = parts[3]
                computed = hashlib.pbkdf2_hmac(
                    "sha256", plain_password.encode("utf-8"), salt_bytes, rounds
                ).hex()
                return hmac.compare_digest(expected_hash, computed)
        except Exception:
            return False

    # Fallback for legacy demo/test records: constant-time string comparison
    return secrets.compare_digest(
        plain_password.strip(), hashed_or_stored.strip()
    ) or secrets.compare_digest(plain_password, hashed_or_stored)


def is_hashed(value: str) -> bool:
    """Returns True if the value appears to be a bcrypt or pbkdf2 hash."""
    if not value or not isinstance(value, str):
        return False
    return (
        value.startswith("$2a$")
        or value.startswith("$2b$")
        or value.startswith("pbkdf2_sha256$")
    )
