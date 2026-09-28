"""
Deployment Readiness & Production Verification Tests for StatSkill AI.
Validates server health probes, OpenAPI specifications, CORS headers,
storage file integrity, admin security keys, and environment fallbacks.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
import pytest
from starlette.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app, DATA_FILE, DEMO_FILE, UPLOAD_DIR, ADMIN_KEY
from services.igot_service import IGOT_COURSE_CATALOG
from services.competency_service import ENGINE_DEFINITIONS

client = TestClient(app)


def test_01_server_health_probe():
    """Verify production liveness probe returns HTTP 200 and healthy status."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ("ok", "healthy")
    assert "version" in data
    assert "platform" in data


def test_02_openapi_json_schema_validity():
    """Verify OpenAPI 3.0 schema is generated cleanly with all endpoints and models."""
    res = client.get("/openapi.json")
    assert res.status_code == 200
    schema = res.json()
    assert "openapi" in schema
    assert "paths" in schema
    assert "/api/auth/login" in schema["paths"]
    assert "/api/mcq/generate" in schema["paths"]
    assert "/api/igot/courses" in schema["paths"]
    assert "/api/assessments/submit" in schema["paths"]


def test_03_swagger_docs_accessible():
    """Verify interactive Swagger API documentation is rendered for deployment."""
    res = client.get("/docs")
    assert res.status_code == 200
    assert "swagger-ui" in res.text.lower()


def test_04_cors_headers_handling():
    """Verify CORS preflight handling permits frontend origin headers."""
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "authorization,content-type",
    }
    res = client.options("/api/auth/login", headers=headers)
    assert res.status_code == 200
    assert "access-control-allow-origin" in res.headers


def test_05_statskill_data_file_integrity():
    """Verify backend storage file exists, parses as valid JSON, and has populated users."""
    assert DATA_FILE.exists(), f"Missing production data file at {DATA_FILE}"
    content = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    assert "users" in content
    assert isinstance(content["users"], list)
    assert len(content["users"]) >= 1, "Dataset must contain at least 1 user record"

    user0 = content["users"][0]
    assert "id" in user0
    assert "profile" in user0
    assert "dashboard" in user0
    assert "competencies" in user0


def test_06_demo_json_credentials_presence():
    """Verify demo.json exists and provides valid demonstration credentials."""
    assert DEMO_FILE.exists(), f"Missing demo configuration file at {DEMO_FILE}"
    demo = json.loads(DEMO_FILE.read_text(encoding="utf-8"))
    assert "user" in demo
    user = demo["user"]
    assert "ananya.verma" in user.get("email", "")
    assert user.get("password") == "Demo@12345"


def test_07_uploads_directory_writable():
    """Verify uploads directory exists and is writable for document ingestion."""
    assert UPLOAD_DIR.exists()
    assert UPLOAD_DIR.is_dir()
    test_probe_file = UPLOAD_DIR / ".write_probe"
    try:
        test_probe_file.write_text("probe", encoding="utf-8")
        assert test_probe_file.read_text(encoding="utf-8") == "probe"
    finally:
        if test_probe_file.exists():
            test_probe_file.unlink()


def test_08_igot_catalog_completeness():
    """Verify iGOT Karmayogi catalog covers core official statistical domains."""
    assert len(IGOT_COURSE_CATALOG) >= 6
    catalog_domains = {c["competency_domain"] for c in IGOT_COURSE_CATALOG}
    for req_domain in ["statisticalMethods", "nationalAccounts", "priceIndices", "dataQuality"]:
        assert req_domain in catalog_domains, f"Missing course coverage for {req_domain}"


def test_09_competency_framework_definitions():
    """Verify FRAC competency framework definitions match official standards."""
    assert len(ENGINE_DEFINITIONS) == 7
    for key, defn in ENGINE_DEFINITIONS.items():
        assert "name" in defn
        assert "benchmark" in defn
        assert "weight" in defn
        assert 1.0 <= defn["benchmark"] <= 5.0
        assert defn["weight"] > 0


def test_10_admin_security_rejection_without_key():
    """Verify Admin endpoints strictly enforce ADMIN_KEY authentication."""
    res = client.get("/api/admin/users")
    assert res.status_code == 403

    res_wrong_key = client.get("/api/admin/users", headers={"X-Admin-Key": "wrong-key-12345"})
    assert res_wrong_key.status_code == 403

    res_valid = client.get("/api/admin/users", headers={"X-Admin-Key": ADMIN_KEY})
    assert res_valid.status_code == 200
    assert "users" in res_valid.json()
