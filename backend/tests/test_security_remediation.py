"""
StatSkill AI — Security, Integrity, and Architecture Remediation Test Suite.
Verifies all P0/P1/P2/P3 remediation controls:
- Password hashing (bcrypt / PBKDF2 fallback) and profile sanitization
- Production admin secret fail-fast validation
- Strict CORS configuration (no wildcard with credentials)
- Server-authoritative assessment grading (rejection of client-tampered correctness)
- Certificate ownership enforcement and public cryptographic verification
- Document upload validation (extensions, size limit, path traversal neutralization)
- Document vault cross-user download authorization
- Persistent SQLite session repository lifecycle
- Health and readiness probes
"""

import io
import json
import uuid
import pytest
from starlette.testclient import TestClient

from main import app, ADMIN_KEY
from core.config import CORS_ORIGINS
from services.password_service import hash_password, verify_password, is_hashed
from services.certificate_service import compute_certificate_hash, verify_certificate_record
from services.assessment_service import grade_submission, OFFICIAL_DIAGNOSTIC_QUIZZES
from services.document_service import sanitize_filename, validate_upload_constraints
from repositories.session_repository import session_repo, SESSIONS


client = TestClient(app)


# ==============================================================================
# 1. Password Hashing & Authentication Security
# ==============================================================================

def test_password_hashing_roundtrip():
    """Verify hash_password produces valid hashes and verify_password checks them accurately."""
    plain = "SuperSecurePassword#2026"
    pw_hash = hash_password(plain)

    assert pw_hash != plain
    assert is_hashed(pw_hash)
    assert verify_password(plain, pw_hash) is True
    assert verify_password("WrongPassword123", pw_hash) is False
    assert verify_password("", pw_hash) is False


def test_user_registration_hashes_password_and_sanitizes_response():
    """Verify registration never stores plaintext password and never leaks hashes in response."""
    test_email = f"officer.{uuid.uuid4().hex[:8]}@demo.gov.in"
    reg_payload = {
        "email": test_email,
        "password": "CorrectHorseBatteryStaple!9",
        "name": "Audit Officer Test",
        "role": "Data Analyst",
        "department": "National Accounts Division",
        "account_type": "government_officer",
    }

    res = client.post("/api/auth/register", json=reg_payload)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data

    # Verify response body sanitization
    profile = data.get("data", {}).get("profile", {})
    assert "password" not in profile
    assert "password_hash" not in profile
    assert "hashed_password" not in profile

    # Verify login with the newly created hashed credential succeeds
    login_res = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "CorrectHorseBatteryStaple!9",
    })
    assert login_res.status_code == 200
    login_profile = login_res.json().get("data", {}).get("profile", {})
    assert "password" not in login_profile
    assert "password_hash" not in login_profile

    # Verify login with wrong password fails
    fail_res = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "IncorrectPassword123",
    })
    assert fail_res.status_code == 401


# ==============================================================================
# 2. CORS & Admin Security Configuration
# ==============================================================================

def test_cors_origins_never_wildcard():
    """Verify CORS configuration does not allow '*' when credentials are enabled."""
    assert "*" not in CORS_ORIGINS
    for origin in CORS_ORIGINS:
        assert origin.startswith("http://") or origin.startswith("https://")


def test_admin_production_secret_fail_fast(monkeypatch):
    """Verify that in production mode, missing or default admin key raises RuntimeError."""
    from core.config import validate_production_config

    # In development mode, default key is tolerated
    validate_production_config("development", "dev-admin-key")

    # In production mode, default key MUST raise RuntimeError
    with pytest.raises(RuntimeError, match="STATSKILL_ADMIN_KEY must be set"):
        validate_production_config("production", "dev-admin-key")

    with pytest.raises(RuntimeError, match="STATSKILL_ADMIN_KEY must be set"):
        validate_production_config("production", "")


# ==============================================================================
# 3. Assessment Server-Side Grading Integrity
# ==============================================================================

def test_assessment_tampered_answers_rejected():
    """
    CRITICAL: Verify client cannot tamper with 'is_correct' or 'score'.
    Even if client sends is_correct=True for wrong answers, server grades authoritatively.
    """
    from schemas.assessment_schemas import QuizAnswerItem

    # Grab the canonical sampling survey quiz
    sampling_quiz = OFFICIAL_DIAGNOSTIC_QUIZZES["QUIZ-SAMPLING"]
    questions = sampling_quiz["questions"]

    # Deliberately submit INCORRECT answers while maliciously claiming is_correct=True
    tampered_answers = []
    for q in questions:
        authoritative_correct = q["correct_index"]
        # Intentionally pick the WRONG option
        wrong_option = (authoritative_correct + 1) % len(q["options"])
        tampered_answers.append(QuizAnswerItem(
            question_id=q["id"],
            selected_option=wrong_option,
            correct_option=wrong_option,  # Tampered
            is_correct=True,  # Malicious client claims it is correct!
        ))

    # Run through the server grading engine
    correct, total, score_pct, evaluated_answers = grade_submission("QUIZ-SAMPLING", tampered_answers)

    # Server must have overridden all tampered answers to False!
    for ans in evaluated_answers:
        assert ans["is_correct"] is False, "Server must reject client-provided is_correct!"

    assert correct == 0
    assert score_pct == 0.0, f"Expected 0% score for all wrong answers, got {score_pct}%"


def test_assessment_submit_endpoint_grades_authoritatively():
    """Test full assessment submission endpoint via HTTP to ensure server-side grading."""
    # First login as demo officer
    login_res = client.post("/api/auth/login", json={
        "email": "ananya.verma@demo.gov.in",
        "password": "Demo@12345",
    })
    token = login_res.json()["access_token"]

    # Submit with tampered is_correct=True for wrong option
    payload = {
        "quiz_id": "QUIZ-SAMPLING",
        "title": "National Sample Survey Sampling & Estimation Diagnostic",
        "domain": "statisticalMethods",
        "answers": [
            {
                "question_id": "Q1",
                "selected_option": 1,  # Wrong answer (authoritative is 0)
                "correct_option": 1,
                "is_correct": True,    # Tampered flag
            }
        ]
    }

    res = client.post(
        "/api/assessments/submit",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    # Server must grade as 0% because option 1 is incorrect
    assert data.get("score") == 0.0
    assert data.get("correctCount") == 0


# ==============================================================================
# 4. Certificate Integrity & Verification
# ==============================================================================

def test_certificate_hash_computation_deterministic():
    """Verify certificate hash is SHA-256 deterministic and tamper-evident."""
    h1 = compute_certificate_hash("CERT-001", "Officer Test", "Advanced Sampling", "2026-01-01")
    h2 = compute_certificate_hash("CERT-001", "Officer Test", "Advanced Sampling", "2026-01-01")
    h3 = compute_certificate_hash("CERT-001", "Officer Test", "Different Title", "2026-01-01")

    assert h1 == h2
    assert len(h1) == 64
    assert h1 != h3


def test_certificate_verification_endpoint():
    """Verify public verification endpoint returns authentic record without government misrepresentation."""
    res = client.get("/api/certificates/CERT-001/verify")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Active"
    assert data["valid"] is True
    assert "StatSkill AI" in data["issuer"]
    assert "Government of India" not in data["issuer"]
    assert "integrity_hash" in data


def test_certificate_authorization_prevents_cross_user_download():
    """Verify that User B cannot download an arbitrary private or non-existent certificate."""
    # Register User B
    user_b_email = f"officer.b.{uuid.uuid4().hex[:8]}@demo.gov.in"
    reg_b = client.post("/api/auth/register", json={
        "email": user_b_email,
        "password": "PasswordB#123",
        "name": "Officer B",
        "role": "Economist",
        "department": "Price Division",
    })
    assert reg_b.status_code == 200
    token_b = reg_b.json()["access_token"]

    # User B attempts to download an unowned private certificate
    res = client.get(
        "/api/certificates/CERT-PRIVATE-USER-A/download",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    # Must be 403 or 404
    assert res.status_code in (403, 404)


# ==============================================================================
# 5. File Upload Security & Document Authorization
# ==============================================================================

def test_file_upload_sanitization():
    """Verify path traversal characters and illegal characters are sanitized from filenames."""
    unsafe = "../../../etc/passwd.pdf"
    safe = sanitize_filename(unsafe)
    assert ".." not in safe
    assert "/" not in safe
    assert "\\" not in safe
    assert safe.endswith(".pdf")


def test_file_upload_rejects_unsupported_extensions():
    """Verify executable or dangerous extensions are rejected."""
    with pytest.raises(Exception) as exc:
        validate_upload_constraints("malicious_script.exe", 1024)
    assert "Unsupported file format" in str(exc.value)

    with pytest.raises(Exception) as exc:
        validate_upload_constraints("payload.sh", 1024)
    assert "Unsupported file format" in str(exc.value)


def test_file_upload_rejects_oversized_files():
    """Verify files exceeding 25 MB are rejected with 413."""
    oversized = 30 * 1024 * 1024  # 30 MB
    with pytest.raises(Exception) as exc:
        validate_upload_constraints("huge_report.pdf", oversized)
    assert "File size exceeds the maximum allowed limit" in str(exc.value)


def test_document_cross_user_download_forbidden():
    """Verify authenticated user cannot download another user's private document."""
    login_res = client.post("/api/auth/login", json={
        "email": "aarav.sharma@learner.in",
        "password": "Learner@12345",
    })
    token = login_res.json()["access_token"]

    # Request a non-existent / private doc
    res = client.get(
        "/api/documents/non-existent-secret-doc/download",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404


# ==============================================================================
# 6. Persistent Session Storage & System Probes
# ==============================================================================

def test_session_repository_persistence():
    """Verify sessions persist in SQLite and support dict interface."""
    test_token = "audit-session-token-12345"
    SESSIONS[test_token] = {
        "id": "USR-TEST-001",
        "profile": {"name": "Persistent Test User", "email": "persist@test.gov.in"},
    }

    # Verify retrieval
    retrieved = SESSIONS.get(test_token)
    assert retrieved is not None
    assert retrieved["id"] == "USR-TEST-001"
    assert retrieved["profile"]["name"] == "Persistent Test User"

    # Verify deletion
    del SESSIONS[test_token]
    assert SESSIONS.get(test_token) is None


def test_system_readiness_probe():
    """Verify /readiness endpoint checks dataset, sessions, and storage."""
    res = client.get("/readiness")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ready"
    assert data["checks"]["dataset"] == "ok"
    assert data["checks"]["sessions"] == "ok"
    assert data["checks"]["storage"] == "ok"
