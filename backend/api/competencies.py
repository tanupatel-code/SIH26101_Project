from typing import Any
from fastapi import APIRouter
from services.competency_service import ENGINE_DEFINITIONS

router = APIRouter(tags=["competencies"])


@router.get("/api/competencies/framework")
def competency_framework() -> dict[str, Any]:
    """Returns the official MoSPI FRAC competency framework definitions and benchmarks."""
    return {
        "framework": "Mission Karmayogi FRAC - MoSPI Official Statistical Cadre",
        "definitions": ENGINE_DEFINITIONS,
    }
