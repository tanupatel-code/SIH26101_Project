"""
StatSkill AI — Persistent Session Repository.
Provides a thread-safe SQLite-backed session store with automatic expiration,
revocation, and backward-compatible mapping semantics.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from typing import Any, Iterator, MutableMapping
from pathlib import Path

from core.config import BASE_DIR

# DB file location
DB_PATH = BASE_DIR / "sessions.db"
DEFAULT_TTL_SECONDS = 7 * 24 * 3600  # 7 days


class SessionRepository:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._lock, self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL,
                    profile_json TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at)"
            )
            conn.commit()

    def create(
        self,
        token: str,
        user_id: str,
        profile: dict[str, Any],
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
    ) -> dict[str, Any]:
        now = time.time()
        expires_at = now + ttl_seconds
        profile_json = json.dumps(profile)
        with self._lock, self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO sessions (token, user_id, created_at, expires_at, profile_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (token, user_id, now, expires_at, profile_json),
            )
            conn.commit()
        return {"id": user_id, "profile": profile, "token": token, "expires_at": expires_at}

    def get(self, token: str) -> dict[str, Any] | None:
        if not token:
            return None
        now = time.time()
        with self._lock, self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT user_id, expires_at, profile_json FROM sessions WHERE token = ?",
                (token,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            if row["expires_at"] < now:
                # Expired session
                conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
                conn.commit()
                return None
            try:
                profile = json.loads(row["profile_json"])
            except Exception:
                profile = {}
            return {
                "id": row["user_id"],
                "profile": profile,
                "token": token,
                "expires_at": row["expires_at"],
            }

    def delete(self, token: str) -> bool:
        if not token:
            return False
        with self._lock, self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
            conn.commit()
            return cursor.rowcount > 0

    def cleanup_expired(self) -> int:
        now = time.time()
        with self._lock, self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM sessions WHERE expires_at < ?", (now,))
            conn.commit()
            return cursor.rowcount

    def clear_all(self) -> None:
        with self._lock, self._get_connection() as conn:
            conn.execute("DELETE FROM sessions")
            conn.commit()


# Singleton repository instance
session_repo = SessionRepository()


class SessionMappingProxy(MutableMapping[str, dict[str, Any]]):
    """
    Backward-compatible dict-like wrapper around SessionRepository so that existing
    tests and callers using SESSIONS[token] or SESSIONS.get(token) continue working.
    """

    def __getitem__(self, key: str) -> dict[str, Any]:
        val = session_repo.get(key)
        if val is None:
            raise KeyError(key)
        return val

    def __setitem__(self, key: str, value: dict[str, Any]) -> None:
        user_id = str(value.get("id") or value.get("user_id") or "USR-DEMO")
        profile = value.get("profile") or {}
        session_repo.create(token=key, user_id=user_id, profile=profile)

    def __delitem__(self, key: str) -> None:
        if not session_repo.delete(key):
            raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        with session_repo._lock, session_repo._get_connection() as conn:
            rows = conn.execute(
                "SELECT token FROM sessions WHERE expires_at > ?", (time.time(),)
            ).fetchall()
            return iter([r["token"] for r in rows])

    def __len__(self) -> int:
        with session_repo._lock, session_repo._get_connection() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM sessions WHERE expires_at > ?",
                (time.time(),),
            ).fetchone()
            return int(row["cnt"]) if row else 0

    def get(self, key: str, default: Any = None) -> Any:
        val = session_repo.get(key)
        return val if val is not None else default

    def pop(self, key: str, default: Any = None) -> Any:
        val = session_repo.get(key)
        if val is not None:
            session_repo.delete(key)
            return val
        return default


# SESSIONS proxy object for backward compatibility
SESSIONS = SessionMappingProxy()
