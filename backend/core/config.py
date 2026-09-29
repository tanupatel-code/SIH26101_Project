"""
StatSkill AI — Centralized Platform Configuration.
Manages environment detection, secure credentials, strict CORS policies,
and upload constraints.
"""

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

# Environment Mode: 'development' | 'production' | 'test'
ENVIRONMENT = os.getenv("STATSKILL_ENV", os.getenv("ENVIRONMENT", "development")).lower().strip()

def validate_production_config(env: str, key: str | None) -> None:
    if env.lower().strip() == "production":
        if not key or key.strip() in {
            "dev-admin-key",
            "default-admin-key",
            "admin",
            "password",
            "12345",
        }:
            raise RuntimeError(
                "FATAL CONFIGURATION ERROR: In production mode, STATSKILL_ADMIN_KEY must be set to a strong secret. "
                "Default development fallback keys are strictly prohibited in production."
            )


# Security & Admin Key
_raw_admin_key = os.getenv("STATSKILL_ADMIN_KEY")
validate_production_config(ENVIRONMENT, _raw_admin_key)
ADMIN_KEY = _raw_admin_key.strip() if _raw_admin_key else "dev-admin-key"

# CORS Configuration — Never use wildcard '*' with credentials
_default_dev_origins = (
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:80,"
    "http://localhost,http://127.0.0.1:80,http://127.0.0.1"
)
_raw_cors = os.getenv("STATSKILL_CORS_ORIGINS", _default_dev_origins)

CORS_ORIGINS: list[str] = [
    origin.strip().rstrip("/")
    for origin in _raw_cors.split(",")
    if origin.strip() and origin.strip() != "*"
]

# Ensure at least valid local origins exist if configured was empty or '*'
if not CORS_ORIGINS:
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1",
    ]

# File Upload Constraints
MAX_UPLOAD_SIZE_BYTES = int(os.getenv("STATSKILL_MAX_UPLOAD_SIZE", 25 * 1024 * 1024))  # 25 MB
ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".docx", ".pptx", ".txt", ".csv"}
