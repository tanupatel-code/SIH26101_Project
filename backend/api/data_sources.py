from typing import Any
from fastapi import APIRouter
from repositories.dataset_repository import read_data_sources

router = APIRouter(tags=["data-sources"])


@router.get("/api/data-sources")
def get_official_data_sources() -> dict[str, Any]:
    """
    Returns the comprehensive catalog of official National Statistical System data sources.
    """
    return read_data_sources()
