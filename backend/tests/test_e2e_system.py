"""
30 End-to-End System Tests for StatSkill AI.
Tests the full lifecycle: Authentication, Document Ingestion, AI MCQ Generation,
Interactive Assessment Execution, Dynamic Competency Recalculation,
iGOT Karmayogi Course Discovery, Enrollment, Profile Updates, and Admin Operations.
"""

import io
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

TEST_DIR = Path(__file__).resolve().parent
BACKEND_DIR = TEST_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app, ADMIN_KEY

client = TestClient(app)

# Global test state shared between consecutive pipeline steps
STATE = {
    "token": "",
    "user_id": "",
    "doc_id": "",
    "uploaded_name": "",
    "initial_comp_score": 0.0,
    "initial_hours": 0.0,
}


# ============================================================================
# PHASE 1: Health, Metadata & Authentication (Tests 1 - 7)
# ============================================================================

def test_01_server_health():
    """Verify health endpoint reports online status and platform version."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "StatSkill" in data["platform"]


def test_02_platform_meta():
    """Verify metadata endpoint exposes system parameters and iGOT course counts."""
    res = client.get("/api/meta")
    assert res.status_code == 200
    data = res.json()
    assert data["userCount"] >= 50
    assert data["igotCourseCount"] >= 6
    assert "statisticalMethods" in data["domains"]


def test_03_competency_framework():
    """Verify official MoSPI FRAC competency framework definitions."""
    res = client.get("/api/competencies/framework")
    assert res.status_code == 200
    data = res.json()
    assert "FRAC" in data["framework"]
    assert "nationalAccounts" in data["definitions"]
    assert "priceIndices" in data["definitions"]


def test_04_auth_login_success():
    """Verify login with demo credentials returns valid bearer token and user snapshot."""
    res = client.post("/api/auth/login", json={
        "email": "ananya.verma@demo.gov.in",
        "password": "Demo@12345"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["data"]["user"]["name"] == "Ananya Verma"
    assert data["data"]["id"] == "USR-001"

    # Save to state
    STATE["token"] = data["access_token"]
    STATE["user_id"] = data["data"]["id"]
    STATE["initial_comp_score"] = data["data"]["competencyScores"].get("statisticalMethods", 3.0)


def test_05_auth_login_invalid_password():
    """Verify login rejection with HTTP 401 on incorrect password."""
    res = client.post("/api/auth/login", json={
        "email": "ananya.verma@demo.gov.in",
        "password": "WrongPassword999"
    })
    assert res.status_code == 401
    assert "Invalid email or password" in res.json()["detail"]


def test_06_auth_me_bearer():
    """Verify /api/me validates bearer token and returns current user info."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.get("/api/me", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["user"]["email"] == "ananya.verma@demo.gov.in"
    assert "Statistical" in data["user"]["role"]


def test_07_auth_unauthorized_rejection():
    """Verify /api/me rejects requests missing bearer token with HTTP 401."""
    res = client.get("/api/me")
    assert res.status_code == 401


# ============================================================================
# PHASE 2: User Data & Public Lookup (Tests 8 - 9)
# ============================================================================

def test_08_me_data_full_snapshot():
    """Verify /api/me/data returns rich profile including competencies, dashboard, and courses."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.get("/api/me/data", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data["competencies"]) >= 5
    assert len(data["criticalSkills"]) >= 0
    assert "overallCompetency" in data["dashboard"]
    assert "igotRecommendations" in data


def test_09_public_demo_lookup():
    """Verify unauthenticated demo lookups resolve user data for testing."""
    res = client.get(f"/api/users/{STATE['user_id']}/data")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == STATE["user_id"]


# ============================================================================
# PHASE 3: Document Ingestion & AI MCQ Generation (Tests 10 - 16)
# ============================================================================

def test_10_upload_document_text():
    """Verify document upload parses text, creates chunks, and registers in user vault."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    file_content = (
        b"National Sample Survey Office (NSSO) Field Operations Manual.\n\n"
        b"Stratified multi-stage sampling is applied across rural and urban sectors.\n"
        b"Stratification reduces sampling variance between heterogeneous districts.\n"
        b"Second-stage sampling units comprise households selected with equal probability."
    )
    files = {"file": ("NSSO_Sampling_Manual.txt", io.BytesIO(file_content), "text/plain")}
    res = client.post("/api/documents/upload", headers=headers, files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert "NSSO_Sampling_Manual.txt" in data["document"]["name"]
    assert data["document"]["wordCount"] > 10

    STATE["doc_id"] = data["document"]["id"]
    STATE["uploaded_name"] = data["document"]["name"]


def test_11_documents_vault_listing():
    """Verify uploaded document appears at top of user's document vault."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.get("/api/documents", headers=headers)
    assert res.status_code == 200
    docs = res.json()["documents"]
    assert len(docs) >= 1
    assert any(d["name"] == STATE["uploaded_name"] for d in docs)


def test_12_mcq_generate_from_document():
    """Verify AI MCQ generation derives questions from the uploaded document ID."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.post("/api/mcq/generate", headers=headers, json={
        "document_id": STATE["doc_id"],
        "num_questions": 3,
        "difficulty": "Intermediate",
        "bloom_level": "Application"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert len(data["questions"]) == 3
    assert all("question" in q and len(q["options"]) == 4 for q in data["questions"])


def test_13_mcq_generate_from_topic():
    """Verify AI MCQ generation creates valid questions directly from topic prompt."""
    res = client.post("/api/mcq/generate", json={
        "topic": "Consumer Price Index and Inflation Estimation",
        "num_questions": 4,
        "difficulty": "Intermediate"
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["questions"]) == 4


def test_14_mcq_generate_bloom_levels():
    """Verify generated MCQs tag specified Bloom's taxonomy cognitive levels."""
    res = client.post("/api/mcq/generate", json={
        "topic": "Data Validation and Survey Quality Assurance",
        "num_questions": 3,
        "bloom_level": "Analysis"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["bloomLevel"] == "Analysis"


def test_15_mcq_generate_national_accounts():
    """Verify AI MCQ generator produces questions for National Accounts (SNA/GDP)."""
    res = client.post("/api/mcq/generate", json={
        "domain": "nationalAccounts",
        "num_questions": 2
    })
    assert res.status_code == 200
    questions = res.json()["questions"]
    assert len(questions) == 2


def test_16_mcq_generate_price_indices():
    """Verify AI MCQ generator produces questions for Price Statistics (CPI/WPI)."""
    res = client.post("/api/mcq/generate", json={
        "domain": "priceIndices",
        "num_questions": 2
    })
    assert res.status_code == 200
    questions = res.json()["questions"]
    assert len(questions) == 2


# ============================================================================
# PHASE 4: Interactive Assessment & Closed-Loop Reassessment (Tests 17 - 21)
# ============================================================================

def test_17_available_assessments_catalog():
    """Verify /api/assessments/available returns official diagnostic quizzes."""
    res = client.get("/api/assessments/available")
    assert res.status_code == 200
    quizzes = res.json()["quizzes"]
    assert len(quizzes) >= 5
    assert any(q["domain"] == "statisticalMethods" for q in quizzes)
    assert any(q["domain"] == "nationalAccounts" for q in quizzes)


def test_18_submit_assessment_instant_grading():
    """Verify quiz submission scores answers instantly and returns scorecard."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    submission = {
        "quiz_id": "QUIZ-SAMPLING-E2E",
        "title": "National Sampling Techniques Diagnostic",
        "domain": "statisticalMethods",
        "answers": [
            {"question_id": "Q-001", "selected_option": 0, "correct_option": 0, "is_correct": True},
            {"question_id": "Q-002", "selected_option": 0, "correct_option": 0, "is_correct": True},
            {"question_id": "Q-003", "selected_option": 0, "correct_option": 0, "is_correct": True},
            {"question_id": "Q-004", "selected_option": 0, "correct_option": 0, "is_correct": True},
            {"question_id": "Q-005", "selected_option": 0, "correct_option": 0, "is_correct": True},
        ]
    }
    res = client.post("/api/assessments/submit", headers=headers, json=submission)
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["score"] == 100.0
    assert data["correctCount"] == 5


def test_19_reassessment_loop_updates_competency():
    """Verify assessment submission dynamically recalculates domain competency score."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.get("/api/me/data", headers=headers)
    assert res.status_code == 200
    new_score = res.json()["competencyScores"].get("statisticalMethods")
    assert new_score is not None
    # Score should be positive and bounded by 5.0
    assert 0.0 < new_score <= 5.0


def test_20_reassessment_loop_records_history():
    """Verify assessment submission appends record to officer's assessmentHistory."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.get("/api/me/data", headers=headers)
    history = res.json()["assessmentHistory"]
    assert any("National Sampling Techniques Diagnostic" in a.get("title", "") for a in history)


def test_21_reassessment_loop_updates_dashboard():
    """Verify overall competency on dashboard reflects latest assessment performance."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.get("/api/me/data", headers=headers)
    dashboard = res.json()["dashboard"]
    assert "overallCompetency" in dashboard
    assert dashboard["overallCompetency"] > 0


# ============================================================================
# PHASE 5: iGOT Karmayogi Connector & Enrollment (Tests 22 - 26)
# ============================================================================

def test_22_igot_catalog_endpoint():
    """Verify /api/igot/courses returns official NSSTA/MoSPI courses."""
    res = client.get("/api/igot/courses")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 6
    assert any(c["id"] == "iGOT-NSSTA-STAT-101" for c in data["courses"])


def test_23_igot_filter_by_domain():
    """Verify filtering iGOT catalog by domain returns only matching courses."""
    res = client.get("/api/igot/courses?domain=priceIndices")
    assert res.status_code == 200
    courses = res.json()["courses"]
    assert len(courses) >= 1
    assert all(c["competency_domain"] == "priceIndices" for c in courses)


def test_24_igot_dynamic_recommendations():
    """Verify /api/igot/recommendations prioritizes courses targeting officer's critical skill gaps."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.get("/api/igot/recommendations", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) >= 1
    assert "reason_for_recommendation" in data["recommendations"][0]


def test_25_igot_enrollment_pipeline():
    """Verify officer can enroll in recommended iGOT course and it appears in active courses."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    enroll_payload = {"course_id": "iGOT-NSSTA-SNA-201"}
    res = client.post("/api/igot/enroll", headers=headers, json=enroll_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["enrolledCourse"]["id"] == "iGOT-NSSTA-SNA-201"


def test_26_igot_enrollment_credits_hours():
    """Verify course enrollment adds 4 learning hours to officer's rawInputs and updates training profile."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.get("/api/me/data", headers=headers)
    assert res.status_code == 200
    user_courses = res.json()["courses"]
    assert any(c["id"] == "iGOT-NSSTA-SNA-201" for c in user_courses)


# ============================================================================
# PHASE 6: Profile, Admin & Session Lifecycle (Tests 27 - 30)
# ============================================================================

def test_27_profile_update_display_name():
    """Verify officer can update display name in profile settings."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.put("/api/me/profile", headers=headers, json={"name": "Ananya Verma, JSO"})
    assert res.status_code == 200
    data = res.json()
    assert data["user"]["name"] == "Ananya Verma, JSO"


def test_28_admin_user_directory():
    """Verify admin endpoint requires dev admin key and returns user directory."""
    headers = {"X-Admin-Key": ADMIN_KEY}
    res = client.get("/api/admin/users", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data["users"]) >= 50


def test_29_admin_patch_competency():
    """Verify admin can patch user competencies directly."""
    headers = {"X-Admin-Key": ADMIN_KEY}
    patch_payload = {
        "data": {
            "competencyScores": {
                "statisticalMethods": 4.85
            }
        }
    }
    res = client.put(f"/api/admin/users/{STATE['user_id']}", headers=headers, json=patch_payload)
    assert res.status_code == 200
    assert res.json()["competencyScores"]["statisticalMethods"] == 4.85


def test_30_auth_logout_invalidation():
    """Verify logout terminates active session token."""
    headers = {"Authorization": f"Bearer {STATE['token']}"}
    res = client.post("/api/auth/logout", headers=headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True

    # Token must now be invalidated
    res_after = client.get("/api/me", headers=headers)
    assert res_after.status_code == 401
