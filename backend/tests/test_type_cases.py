"""
Type Case & Schema Validation Tests for StatSkill AI.
Verifies strict type safety, Pydantic schema validation, edge case type coercion,
and HTTP 422 Unprocessable Entity responses for malformed payloads.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
import pytest
from pydantic import ValidationError
from starlette.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import (
    app,
    LoginRequest,
    RegisterRequest,
    McqGenerateRequest,
    QuizSubmitRequest,
    QuizAnswerItem,
    AdminUserPatch,
    EnrollRequest,
    UserUpdateRequest,
)
from services.competency_service import (
    is_number,
    avg,
    calculate_competency_scores,
    ensure_competency_shape,
)
from services.document_parser import chunk_document, extract_text_from_txt
from services.igot_service import get_all_courses, recommend_courses_for_gaps

client = TestClient(app)


# ==========================================
# 1. Pydantic Model Schema & Type Unit Tests
# ==========================================

def test_login_request_valid_types():
    req = LoginRequest(email="ananya.verma@mospi.gov.in", password="ValidPassword123")
    assert isinstance(req.email, str)
    assert isinstance(req.password, str)


def test_login_request_invalid_types_raise_validation_error():
    with pytest.raises(ValidationError):
        LoginRequest(email="", password="123")  # email min_length is 3

    with pytest.raises(ValidationError):
        LoginRequest(email="valid@test.gov", password="")  # password min_length is 1


def test_register_request_validation_and_defaults():
    req = RegisterRequest(
        name="Sunil Rao",
        email="sunil.rao@mospi.gov.in",
        password="SecurePassword99",
    )
    assert req.role == "Statistical Investigator"
    assert req.department == "MoSPI"
    assert req.projectId == "SIH26101"
    assert len(req.password) >= 6


def test_register_request_short_password_rejected():
    with pytest.raises(ValidationError):
        RegisterRequest(
            name="A",
            email="a@b.com",
            password="123",  # Under 6 characters
        )


def test_mcq_generate_request_bounds():
    valid = McqGenerateRequest(num_questions=5, difficulty="Intermediate", domain="statisticalMethods")
    assert valid.num_questions == 5

    # Out of bounds: 0 questions
    with pytest.raises(ValidationError):
        McqGenerateRequest(num_questions=0)

    # Out of bounds: > 20 questions
    with pytest.raises(ValidationError):
        McqGenerateRequest(num_questions=25)


def test_quiz_answer_item_type_checking():
    item = QuizAnswerItem(
        question_id="MCQ-001",
        selected_option=2,
        correct_option=2,
        is_correct=True,
    )
    assert isinstance(item.selected_option, int)
    assert isinstance(item.is_correct, bool)

    # String passed to int selected_option should fail if non-numeric
    with pytest.raises(ValidationError):
        QuizAnswerItem(
            question_id="MCQ-001",
            selected_option="not-an-int",  # type: ignore[arg-type]
            correct_option=1,
            is_correct=False,
        )


def test_quiz_submit_request_schema():
    payload = {
        "quiz_id": "QUIZ-TEST",
        "title": "National Accounts Test",
        "domain": "nationalAccounts",
        "answers": [
            {
                "question_id": "MCQ-01",
                "selected_option": 1,
                "correct_option": 1,
                "is_correct": True,
            }
        ],
    }
    submit_req = QuizSubmitRequest(**payload)
    assert len(submit_req.answers) == 1
    assert submit_req.answers[0].is_correct is True


def test_quiz_submit_request_invalid_answers_type():
    with pytest.raises(ValidationError):
        QuizSubmitRequest(
            quiz_id="QUIZ-TEST",
            title="Invalid Answers",
            domain="statisticalMethods",
            answers="this-is-not-a-list",  # type: ignore[arg-type]
        )


def test_admin_user_patch_requires_dict():
    patch = AdminUserPatch(data={"role": "Senior Statistical Officer"})
    assert isinstance(patch.data, dict)

    with pytest.raises(ValidationError):
        AdminUserPatch(data="string_not_dict")  # type: ignore[arg-type]


def test_enroll_request_type_safety():
    req = EnrollRequest(course_id="iGOT-NSSTA-STAT-101")
    assert req.course_id == "iGOT-NSSTA-STAT-101"

    with pytest.raises(ValidationError):
        EnrollRequest()  # missing course_id


# ==========================================
# 2. HTTP 422 Unprocessable Entity Endpoint Tests
# ==========================================

def test_http_422_on_login_empty_payload():
    res = client.post("/api/auth/login", json={})
    assert res.status_code == 422
    assert "detail" in res.json()


def test_http_422_on_login_type_mismatch():
    res = client.post("/api/auth/login", json={"email": "ab", "password": 123})
    assert res.status_code == 422


def test_http_422_on_register_short_password():
    res = client.post(
        "/api/auth/register",
        json={"name": "Test", "email": "test@domain.com", "password": "123"},
    )
    assert res.status_code == 422


def test_http_422_on_mcq_generate_invalid_number_type():
    res = client.post("/api/mcq/generate", json={"num_questions": "invalid_number_str"})
    assert res.status_code == 422


def test_http_422_on_mcq_generate_negative_questions():
    res = client.post("/api/mcq/generate", json={"num_questions": -5})
    assert res.status_code == 422


def test_http_422_on_mcq_generate_excessive_questions():
    res = client.post("/api/mcq/generate", json={"num_questions": 100})
    assert res.status_code == 422


def test_http_422_on_assessment_submit_malformed_answers():
    res = client.post(
        "/api/assessments/submit",
        json={
            "quiz_id": "QUIZ-TEST",
            "answers": [{"question_id": "Q1", "selected_option": "not_an_int"}],
        },
    )
    assert res.status_code == 422


def test_http_422_on_enroll_missing_body():
    res = client.post("/api/igot/enroll", json={})
    assert res.status_code == 422


# ==========================================
# 3. Service Type Safety & Null Guard Tests
# ==========================================

def test_is_number_type_guards():
    assert is_number(5) is True
    assert is_number(3.14159) is True
    assert is_number("42") is True
    assert is_number("3.85") is True
    assert is_number(0) is True
    assert is_number(-10.5) is True

    # Invalid types
    assert is_number(None) is False
    assert is_number("not_a_number") is False
    assert is_number([]) is False
    assert is_number({}) is False
    assert is_number(float("nan")) is False
    assert is_number(float("inf")) is False


def test_avg_type_guards():
    assert avg([10, 20, 30]) == 20.0
    assert avg(["10", "20", 30.0]) == 20.0
    assert avg([]) == 0.0
    assert avg([None, "abc", {}]) == 0.0
    assert avg([50, None, 100]) == 75.0


def test_calculate_competency_scores_handles_corrupted_raw_inputs():
    corrupted_record: dict[str, Any] = {
        "rawInputs": {
            "selfAssessment": None,
            "learningHours": "not-a-dict",
        },
        "assessmentHistory": None,
        "courses": "invalid-type",
    }
    scores = calculate_competency_scores(corrupted_record)
    assert isinstance(scores, dict)
    for domain, score in scores.items():
        assert isinstance(score, float)
        assert 0.0 <= score <= 5.0


def test_ensure_competency_shape_type_coercion():
    record: dict[str, Any] = {
        "id": "USR-TEST-TYPE",
        "competencyScores": {
            "statisticalMethods": "3.8",  # string type instead of float
            "nationalAccounts": 4,        # integer type instead of float
        },
    }
    ensure_competency_shape(record)
    assert isinstance(record["competencies"], list)
    for c in record["competencies"]:
        assert isinstance(c["score"], float)
        assert isinstance(c["benchmark"], float)
        assert isinstance(c["gap"], float)
        assert isinstance(c["weight"], float)


def test_chunk_document_type_safety():
    assert chunk_document("") == []
    assert chunk_document("   \n\n  ") == []
    chunks = chunk_document("Sample text paragraph one.\n\nSample text paragraph two.", chunk_size=500, overlap=50)
    assert isinstance(chunks, list)
    for ch in chunks:
        assert isinstance(ch["chunk_id"], int)
        assert isinstance(ch["text"], str)
        assert isinstance(ch["length"], int)


def test_extract_text_from_txt_encodings():
    utf8_bytes = "Statistical System of India: MoSPI".encode("utf-8")
    assert "Statistical System" in extract_text_from_txt(utf8_bytes)

    latin1_bytes = "Café National Accounts".encode("latin-1")
    assert "National Accounts" in extract_text_from_txt(latin1_bytes)


def test_igot_service_type_resilience():
    # Case insensitive domain/level filtering
    courses = get_all_courses(domain="statisticalmethods", level="intermediate")
    assert isinstance(courses, list)

    # Empty gaps input should return safe recommendations
    recs = recommend_courses_for_gaps([], None)
    assert isinstance(recs, list)
    assert len(recs) >= 1
    for r in recs:
        assert isinstance(r["id"], str)
        assert isinstance(r["rating"], (int, float))
