"""
StatSkill AI — Assessment Lifecycle Integrity & Competency Flow Tests.
Verifies server-authoritative quiz grading, replay protection, domain enforcement,
admin override lifecycle, MCQ quality filtering without fake distractors,
and MCQ provider abstraction.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

TEST_DIR = Path(__file__).resolve().parent
BACKEND_DIR = TEST_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app
from services.mcq_generator import validate_and_sanitize_mcqs
from services.mcq_providers import LocalMCQProvider, CompositeMCQProvider
from repositories.user_repository import user_repo
from services.competency_service import ensure_competency_shape, calculate_competency_scores


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_header(client: TestClient) -> dict[str, str]:
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "ananya.verma@demo.gov.in", "password": "Demo@12345"},
    )
    assert login_resp.status_code == 200, "Fixture login failed"
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# =========================================================================
# 1. Assessment Lifecycle & Grading Integrity
# =========================================================================

def test_unknown_assessment_id_rejected(client: TestClient, auth_header: dict[str, str]) -> None:
    """Server must reject an unknown assessment ID with HTTP 400."""
    payload = {
        "quiz_id": "QUIZ-NONEXISTENT-999",
        "domain": "statisticalMethods",
        "answers": [
            {"question_id": "Q1", "selected_option": 0}
        ],
    }
    resp = client.post("/api/assessments/submit", json=payload, headers=auth_header)
    assert resp.status_code == 400
    assert "Unknown assessment" in resp.json()["detail"]


def test_question_not_in_assessment_rejected(client: TestClient, auth_header: dict[str, str]) -> None:
    """Server must reject answers containing question IDs from other quizzes."""
    payload = {
        "quiz_id": "QUIZ-SAMPLING",
        "domain": "statisticalMethods",
        "answers": [
            {"question_id": "Q_SNA_01", "selected_option": 0}  # Belongs to QUIZ-SNA, not QUIZ-SAMPLING
        ],
    }
    resp = client.post("/api/assessments/submit", json=payload, headers=auth_header)
    assert resp.status_code == 400
    assert "does not belong to assessment" in resp.json()["detail"]


def test_invalid_option_index_rejected(client: TestClient, auth_header: dict[str, str]) -> None:
    """Server must reject options outside the allowed range [-1, 3]."""
    payload = {
        "quiz_id": "QUIZ-SAMPLING",
        "domain": "statisticalMethods",
        "answers": [
            {"question_id": "Q1", "selected_option": 99}
        ],
    }
    resp = client.post("/api/assessments/submit", json=payload, headers=auth_header)
    assert resp.status_code == 400
    assert "Invalid option index" in resp.json()["detail"]


def test_duplicate_question_answers_rejected(client: TestClient, auth_header: dict[str, str]) -> None:
    """Server must reject duplicate answers for the same question within a submission."""
    payload = {
        "quiz_id": "QUIZ-SAMPLING",
        "domain": "statisticalMethods",
        "answers": [
            {"question_id": "Q1", "selected_option": 1},
            {"question_id": "Q1", "selected_option": 2},
        ],
    }
    resp = client.post("/api/assessments/submit", json=payload, headers=auth_header)
    assert resp.status_code == 400
    assert "duplicate answer" in resp.json()["detail"].lower()


def test_replay_submission_protection(client: TestClient, auth_header: dict[str, str]) -> None:
    """Submitting the exact same quiz within 2 seconds must be rejected with HTTP 409."""
    # Ensure replay buffer is clear
    time.sleep(2.1)
    payload = {
        "quiz_id": "QUIZ-SAMPLING",
        "domain": "statisticalMethods",
        "answers": [
            {"question_id": "Q1", "selected_option": 1}
        ],
    }
    # First submission
    resp1 = client.post("/api/assessments/submit", json=payload, headers=auth_header)
    assert resp1.status_code == 200

    # Immediate second submission (replay)
    resp2 = client.post("/api/assessments/submit", json=payload, headers=auth_header)
    assert resp2.status_code == 409
    assert "duplicate assessment submission" in resp2.json()["detail"].lower()


def test_server_authoritative_domain_enforcement(client: TestClient, auth_header: dict[str, str]) -> None:
    """Client cannot spoof the competency domain of a known quiz."""
    # Wait out the 2-second replay window
    time.sleep(2.1)

    # Attempt to forge domain as 'machineLearning' for QUIZ-SAMPLING (which is statisticalMethods)
    payload = {
        "quiz_id": "QUIZ-SAMPLING",
        "domain": "machineLearning",  # Forged!
        "answers": [
            {"question_id": "Q1", "selected_option": 1}
        ],
    }
    resp = client.post("/api/assessments/submit", json=payload, headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    # The server must have evaluated and stored the submission under statisticalMethods
    assert data["domain"] == "statisticalMethods"


# =========================================================================
# 2. Competency Engine: Overrides & Authoritative Flow
# =========================================================================

def test_admin_override_lifecycle(client: TestClient, auth_header: dict[str, str]) -> None:
    """
    Test: Raw Evidence -> Calculated Score -> Admin Override -> Clear Override -> Restored Evidence.
    """
    user_record = user_repo.find_by_id("USR-001")
    assert user_record is not None

    # 1. Inspect calculated baseline score
    calculated_scores = calculate_competency_scores(user_record)
    baseline_calc = calculated_scores.get("statisticalMethods", 3.0)

    # 2. Apply admin override to 4.9
    admin_headers = {"x-admin-key": "dev-admin-key"}
    patch_resp = client.patch(
        "/api/admin/users/USR-001",
        json={"data": {"adminOverrides": {"statisticalMethods": 4.9}}},
        headers=admin_headers,
    )
    assert patch_resp.status_code == 200

    # Verify override is reflected in user profile
    profile_resp = client.get("/api/me/data", headers=auth_header)
    assert profile_resp.status_code == 200
    comp_list = profile_resp.json()["competencies"]
    stat_comp = next((c for c in comp_list if c["key"] == "statisticalMethods"), None)
    assert stat_comp is not None
    assert stat_comp["score"] == 4.9

    # 3. Explicitly clear/remove the override
    clear_resp = client.patch(
        "/api/admin/users/USR-001",
        json={"data": {"adminOverrides": {"statisticalMethods": None}}},
        headers=admin_headers,
    )
    assert clear_resp.status_code == 200

    # Verify score reverts back to calculated baseline
    profile_revert = client.get("/api/me/data", headers=auth_header)
    assert profile_revert.status_code == 200
    comp_revert = profile_revert.json()["competencies"]
    stat_revert = next((c for c in comp_revert if c["key"] == "statisticalMethods"), None)
    assert stat_revert is not None
    assert stat_revert["score"] == baseline_calc


def test_unauthorized_user_cannot_set_admin_overrides(client: TestClient, auth_header: dict[str, str]) -> None:
    """Regular users cannot set admin overrides via user endpoints."""
    # Attempt through PUT /api/me/profile
    resp = client.put(
        "/api/me/profile",
        json={"name": "Ananya Verma", "adminOverrides": {"machineLearning": 5.0}},
        headers=auth_header,
    )
    assert resp.status_code == 200
    user_record = user_repo.find_by_id("USR-001")
    assert user_record is not None
    overrides = user_record.get("adminOverrides", {})
    assert overrides.get("machineLearning") != 5.0

    # Attempt directly hitting /api/admin/users without admin key
    admin_resp = client.patch(
        "/api/admin/users/USR-001",
        json={"data": {"adminOverrides": {"machineLearning": 5.0}}},
    )
    assert admin_resp.status_code == 403


# =========================================================================
# 3. MCQ Sanitization & Quality (No Fake Distractors)
# =========================================================================

def test_validate_and_sanitize_mcqs_rejects_insufficient_options() -> None:
    """Questions with fewer than 4 genuine options must be rejected, not filled with dummy options."""
    bad_questions = [
        {
            "id": "Q_BAD_1",
            "question": "What is the primary objective of NSSO?",
            "options": ["Socio-economic surveys", "Price monitoring"],  # Only 2 options
            "correctAnswer": 0,
            "domain": "statisticalMethods",
            "bloomLevel": "Understand",
            "explanation": "NSSO conducts large scale sample surveys for socio-economic planning.",
        }
    ]
    cleaned = validate_and_sanitize_mcqs(bad_questions)
    assert len(cleaned) == 0, "Question with only 2 options should be rejected"


def test_validate_and_sanitize_mcqs_rejects_duplicate_options() -> None:
    """Questions with duplicate options must be rejected."""
    duplicate_options_q = [
        {
            "id": "Q_BAD_2",
            "question": "What measure of central tendency is least affected by extreme values?",
            "options": ["Median", "Median", "Mean", "Mode"],  # Duplicate 'Median'
            "correctAnswer": 0,
            "domain": "statisticalMethods",
            "bloomLevel": "Analyze",
            "explanation": "Median is robust to outliers compared to the arithmetic mean.",
        }
    ]
    cleaned = validate_and_sanitize_mcqs(duplicate_options_q)
    assert len(cleaned) == 0, "Question with duplicate options should be rejected"


def test_validate_and_sanitize_mcqs_accepts_high_quality_question() -> None:
    """Valid questions meeting all psychometric criteria must be preserved."""
    good_questions = [
        {
            "id": "Q_GOOD_1",
            "question": "Which sampling technique ensures proportional representation across heterogeneous administrative strata?",
            "options": [
                "Simple Random Sampling with Replacement",
                "Stratified Multi-stage Probability Proportional to Size Sampling",
                "Convenience Judgement Sampling",
                "Snowball Network Sampling",
            ],
            "correctAnswer": 1,
            "domain": "statisticalMethods",
            "bloomLevel": "Apply",
            "explanation": "Stratified multi-stage sampling divides the population into homogeneous strata to minimize standard error.",
        }
    ]
    cleaned = validate_and_sanitize_mcqs(good_questions)
    assert len(cleaned) == 1
    assert cleaned[0]["correctAnswer"] == 1
    assert cleaned[0]["domain"] == "statisticalMethods"


# =========================================================================
# 4. MCQ Provider Abstraction
# =========================================================================

def test_local_mcq_provider_contract() -> None:
    """LocalMCQProvider must generate valid MCQs with normalized schema and provider metadata."""
    provider = LocalMCQProvider()
    questions = provider.generate_mcqs(
        text="The National Sample Survey Office uses multistage stratified sampling for household surveys.",
        domain="statisticalMethods",
        difficulty="Intermediate",
        count=2,
    )
    assert len(questions) >= 1
    for q in questions:
        assert len(q["options"]) == 4
        assert 0 <= q["correctAnswer"] <= 3
        assert q["_provider"] == "local_rule_based"
        assert q["domain"] == "statisticalMethods"


def test_composite_mcq_provider_fallback() -> None:
    """CompositeMCQProvider must fall back to local rule-based generator when cloud APIs are unconfigured."""
    composite = CompositeMCQProvider()
    questions = composite.generate_mcqs(
        text="Consumer Price Index measures changes over time in general level of retail prices.",
        domain="priceIndices",
        difficulty="Advanced",
        count=2,
    )
    assert len(questions) >= 1
    assert all(len(q["options"]) == 4 for q in questions)
    assert any(q.get("_provider") in ("gemini", "openai", "local", "local_rule_based") for q in questions)
