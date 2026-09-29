from __future__ import annotations

from typing import Any
from fastapi import APIRouter

from repositories.dataset_repository import read_dataset
from services.competency_service import ENGINE_DEFINITIONS
from services.igot_service import IGOT_COURSE_CATALOG

router = APIRouter(tags=["System"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "platform": "StatSkill AI", "version": "3.0.0"}


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
