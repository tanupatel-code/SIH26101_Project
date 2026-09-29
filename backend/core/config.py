from __future__ import annotations

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = Path(os.getenv("STATSKILL_DATA_FILE", BASE_DIR / "statskill.json"))
DEMO_FILE = Path(os.getenv("STATSKILL_DEMO_FILE", BASE_DIR / "demo.json"))
DATA_SOURCES_FILE = Path(
    os.getenv("STATSKILL_DATA_SOURCES_FILE", BASE_DIR / "data_sources.json")
)
UPLOAD_DIR = Path(os.getenv("STATSKILL_UPLOAD_DIR", BASE_DIR / "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Security and Credentials
ADMIN_KEY = os.getenv("STATSKILL_ADMIN_KEY", "dev-admin-key")

# CORS Allowed Origins
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "STATSKILL_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:80,http://localhost",
    ).split(",")
    if origin.strip()
]
CORS_ORIGIN_REGEX = r"https?://(localhost|127\.0\.0\.1)(:\d+)?$"
