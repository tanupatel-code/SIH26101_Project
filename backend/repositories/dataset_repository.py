from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any
from fastapi import HTTPException

from core.config import DATA_FILE, DEMO_FILE, DATA_SOURCES_FILE

DATA_LOCK = Lock()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise HTTPException(status_code=500, detail=f"Data file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_dataset() -> dict[str, Any]:
    with DATA_LOCK:
        return read_json(DATA_FILE)


def write_dataset(data: dict[str, Any]) -> None:
    with DATA_LOCK:
        write_json(DATA_FILE, data)


def read_demo() -> dict[str, Any]:
    return read_json(DEMO_FILE)


def read_data_sources() -> dict[str, Any]:
    if DATA_SOURCES_FILE.exists():
        try:
            return json.loads(DATA_SOURCES_FILE.read_text(encoding="utf-8"))
        except Exception as exc:
            raise HTTPException(
                status_code=500, detail=f"Failed to read data sources: {exc}"
            ) from exc
    return {"title": "Official Statistical Data Sources", "data_sources": []}
