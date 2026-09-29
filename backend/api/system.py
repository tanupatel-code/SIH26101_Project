from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Response, status

from core.config import UPLOAD_DIR
from repositories.dataset_repository import read_dataset
from repositories.session_repository import session_repo
from services.competency_service import ENGINE_DEFINITIONS
from services.igot_service import IGOT_COURSE_CATALOG

router = APIRouter(tags=["System"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "platform": "StatSkill AI", "version": "3.0.0"}


@router.get("/readiness")
def readiness(response: Response) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    is_ready = True

    # 1. Dataset check
    try:
        data = read_dataset()
        checks["dataset"] = "ok" if "users" in data else "missing_users"
    except Exception as exc:
        checks["dataset"] = f"error: {exc}"
        is_ready = False

    # 2. Session store check
    try:
        with session_repo._lock, session_repo._get_connection() as conn:
            conn.execute("SELECT 1 FROM sessions LIMIT 1")
        checks["sessions"] = "ok"
    except Exception as exc:
        checks["sessions"] = f"error: {exc}"
        is_ready = False

    # 3. Storage directory check
    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        checks["storage"] = "ok" if UPLOAD_DIR.exists() else "not_found"
    except Exception as exc:
        checks["storage"] = f"error: {exc}"
        is_ready = False

    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unready", "checks": checks}

    return {"status": "ready", "checks": checks}


@router.get("/api/meta")
def meta() -> dict[str, Any]:
    dataset = read_dataset()
    return {
        "title": "StatSkill AI — Official Statistical Competency Platform",
        "description": "Integrated National Statistical System Capacity Building & Assessment System",
        "dataset": dataset.get("dataset"),
        "version": dataset.get("version", "3.0.0"),
        "userCount": len(dataset.get("users", [])),
        "domains": list(ENGINE_DEFINITIONS.keys()),
        "igotCourseCount": len(IGOT_COURSE_CATALOG),
    }
