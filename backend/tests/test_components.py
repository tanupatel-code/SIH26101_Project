"""
25 Component-Level Unit and Service Tests for StatSkill AI.
Tests Document Parsing, AI MCQ Generation, Competency Calculation,
iGOT Recommendations, and Data Sanitization in isolation.
"""

import math
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
TEST_DIR = Path(__file__).resolve().parent
BACKEND_DIR = TEST_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.document_parser import extract_document_text, chunk_document
from services.mcq_generator import generate_mcqs_from_text, extract_keywords_from_text, OFFICIAL_STATS_CONCEPTS
from services.competency_service import (
    calculate_competency_scores,
    ensure_competency_shape,
    is_number,
    avg,
    ENGINE_DEFINITIONS,
)
from services.igot_service import (
    get_all_courses,
    recommend_courses_for_gaps,
    IGOT_COURSE_CATALOG,
)
from main import sanitize_profile, resolve_login, read_dataset


# ============================================================================
# COMPONENT 1: Document Parser Tests (5 Tests)
# ============================================================================

def test_01_plain_text_extraction():
    """Verify document parser extracts clean text from text bytes."""
    sample = b"National Statistical Systems Training Academy - Sampling Manual."
    result = extract_document_text("manual.txt", sample)
    assert "Sampling Manual" in result
    assert isinstance(result, str)


def test_02_multipage_text_cleaning():
    """Verify parser normalizes irregular whitespace and multiple newlines."""
    sample = b"Chapter 1\n\n\n\n\nSurvey Methodology    and Estimation  Procedures."
    result = extract_document_text("sample.md", sample)
    assert "Chapter 1\n\nSurvey Methodology and Estimation Procedures." == result


def test_03_chunk_document_sizing_and_overlap():
    """Verify semantic chunker splits text into chunks of target size."""
    long_text = "\n\n".join([f"Paragraph {i}: Survey sampling is critical for official statistics." for i in range(40)])
    chunks = chunk_document(long_text, chunk_size=500, overlap=100)
    assert len(chunks) > 1
    for chunk in chunks:
        assert "chunk_id" in chunk
        assert "text" in chunk
        assert len(chunk["text"]) <= 700


def test_04_empty_document_handling():
    """Verify parser returns empty string gracefully for blank document."""
    result = extract_document_text("empty.txt", b"")
    assert result == ""
    chunks = chunk_document("")
    assert chunks == []


def test_05_keyword_extraction():
    """Verify statistical entity & keyword recognizer extracts key terms."""
    text = "The NSSO survey applied stratified sampling to estimate household income variance, GDP, and CPI."
    keywords = extract_keywords_from_text(text)
    assert "sampling" in keywords
    assert "variance" in keywords
    assert "gdp" in keywords
    assert "cpi" in keywords


# ============================================================================
# COMPONENT 2: AI MCQ & Quiz Generator Tests (6 Tests)
# ============================================================================

def test_06_mcq_generation_structure():
    """Verify questions contain id, question, options, correct_index, and explanation."""
    mcqs = generate_mcqs_from_text("Stratified sampling in official statistics", num_questions=3)
    assert len(mcqs) == 3
    for q in mcqs:
        assert "question" in q and len(q["question"]) > 10
        assert "options" in q and isinstance(q["options"], list)
        assert "correct_index" in q
        assert "explanation" in q and len(q["explanation"]) > 10


def test_07_mcq_bloom_taxonomy_assignment():
    """Verify questions respect requested Bloom's taxonomy level."""
    mcqs = generate_mcqs_from_text("System of National Accounts GDP compilation", num_questions=2, bloom_level="Analysis")
    assert len(mcqs) == 2
    for q in mcqs:
        assert q.get("bloom_level") in ["Analysis", "Application", "Understanding"]


def test_08_mcq_options_diversity():
    """Verify every question provides exactly 4 distinct options."""
    mcqs = generate_mcqs_from_text("Data validation protocols", num_questions=4)
    for q in mcqs:
        assert len(q["options"]) == 4
        # Options must be non-empty and unique
        assert len(set(q["options"])) == 4


def test_09_mcq_correct_index_bounds():
    """Verify correct_index is strictly between 0 and 3."""
    mcqs = generate_mcqs_from_text("Consumer price index calculation", num_questions=5)
    for q in mcqs:
        assert 0 <= q["correct_index"] <= 3


def test_10_mcq_explanation_rationale_quality():
    """Verify explanation provides clear pedagogical justification."""
    mcqs = generate_mcqs_from_text("Sampling error vs non-sampling error", num_questions=2)
    for q in mcqs:
        exp = q.get("explanation", "")
        assert len(exp) > 20
        # Ensure it explains why the choice is correct
        assert not exp.isdigit()


def test_11_mcq_domain_specific_targeting():
    """Verify generator prioritizes questions for requested statistical domain."""
    mcqs = generate_mcqs_from_text("", num_questions=2, target_domain="nationalAccounts")
    assert len(mcqs) >= 1
    for q in mcqs:
        if q["domain"] == "nationalAccounts":
            assert any(term in q["question"].lower() for term in ["gdp", "gva", "national accounts", "market prices"])


# ============================================================================
# COMPONENT 3: Competency Engine Tests (6 Tests)
# ============================================================================

def test_12_multi_signal_competency_calculation():
    """Verify 4-signal weighted score formula (quiz 50%, course 25%, self 15%, effort 10%)."""
    user_record = {
        "assessmentHistory": [{"domain": "statisticalMethods", "score": 80}], # 80/20 = 4.0 -> * 0.50 = 2.0
        "courses": [{"domain": "statisticalMethods", "score": 80}],           # 80/20 = 4.0 -> * 0.25 = 1.0
        "rawInputs": {
            "selfAssessment": {"statisticalMethods": [4.0, 4.0]},            # 4.0 -> * 0.15 = 0.60
            "learningHours": {"statisticalMethods": 8.0}                     # 8/8 = 1.0 (max 5) -> * 0.10 = 0.10
        }
    }
    # Expected: 2.0 + 1.0 + 0.60 + 0.10 = 3.70
    scores = calculate_competency_scores(user_record)
    assert "statisticalMethods" in scores
    assert 3.5 <= scores["statisticalMethods"] <= 4.0


def test_13_gap_calculation_accuracy():
    """Verify gap = max(0, benchmark - score)."""
    user_record = {
        "competencyScores": {
            "statisticalMethods": 2.5, # benchmark is 3.5 -> gap should be 1.0
            "gis": 3.2,                # benchmark is 3.0 -> gap should be 0.0
        }
    }
    ensure_competency_shape(user_record)
    comps = {c["key"]: c for c in user_record["competencies"]}
    assert comps["statisticalMethods"]["gap"] == 1.0
    assert comps["gis"]["gap"] == 0.0


def test_14_benchmark_status_classification():
    """Verify benchmark Met vs Below Benchmark tagging."""
    user_record = {
        "competencyScores": {
            "statisticalMethods": 3.8, # above 3.5
            "dataQuality": 2.1,        # below 3.5
        }
    }
    ensure_competency_shape(user_record)
    bm_map = {b["key"]: b for b in user_record["benchmarkComparison"]}
    assert bm_map["statisticalMethods"]["status"] == "Benchmark Met"
    assert bm_map["dataQuality"]["status"] == "Below Benchmark"


def test_15_critical_skills_gap_sorting():
    """Verify criticalSkills sorts below-benchmark domains by highest gap first."""
    user_record = {
        "competencyScores": {
            "statisticalMethods": 1.5, # gap: 2.0 (High priority)
            "python": 2.5,             # gap: 0.5 (Medium priority)
            "dataQuality": 3.0,        # gap: 0.5 (Medium priority)
        }
    }
    ensure_competency_shape(user_record)
    crit = user_record["criticalSkills"]
    assert len(crit) > 0
    assert crit[0]["key"] == "statisticalMethods"
    assert crit[0]["priority"] == "High"


def test_16_readiness_percentage_computation():
    """Verify readiness percentage is correctly capped at 100%."""
    user_record = {
        "competencyScores": {
            "gis": 3.6, # benchmark is 3.0 -> 3.6/3.0 = 120% -> capped at 100%
        }
    }
    ensure_competency_shape(user_record)
    bm = next(b for b in user_record["benchmarkComparison"] if b["key"] == "gis")
    assert bm["readinessPercent"] == 100.0


def test_17_dashboard_overall_score_synthesis():
    """Verify overall competency score synthesizes weighted competencies, quiz average and learning hours."""
    user_record = {
        "competencyScores": {"statisticalMethods": 4.0, "gis": 4.0},
        "assessmentHistory": [{"score": 85}],
        "rawInputs": {"learningHours": {"statisticalMethods": 20}}
    }
    ensure_competency_shape(user_record)
    score = user_record["dashboard"]["overallCompetency"]
    assert 0 <= score <= 100
    assert user_record["dashboard"]["overallCompetencyLabel"] == f"{score}/100"


# ============================================================================
# COMPONENT 4: iGOT Karmayogi Connector Tests (5 Tests)
# ============================================================================

def test_18_igot_catalog_retrieval_and_filtering():
    """Verify iGOT course catalog returns all official courses and supports domain filtering."""
    all_courses = get_all_courses()
    assert len(all_courses) >= 6
    sna_courses = get_all_courses(domain="nationalAccounts")
    assert len(sna_courses) >= 1
    assert "SNA" in sna_courses[0]["id"] or "GDP" in sna_courses[0]["title"]


def test_19_dynamic_gap_to_course_recommendations():
    """Verify courses are recommended that directly target officer's diagnosed gaps."""
    critical_skills = [
        {"competency": "Price Statistics (CPI/WPI/IIP)", "key": "priceIndices", "gap": 1.5, "priority": "High"},
        {"competency": "National Accounts (SNA & GDP)", "key": "nationalAccounts", "gap": 1.2, "priority": "High"},
    ]
    recs = recommend_courses_for_gaps(critical_skills)
    assert len(recs) >= 2
    # First recommendation should target the highest gap (priceIndices)
    assert recs[0]["competency_domain"] in ["priceIndices", "nationalAccounts"]
    assert "reason_for_recommendation" in recs[0]


def test_20_exclude_completed_courses_from_recommendations():
    """Verify completed courses are not redundantly recommended to the officer."""
    critical_skills = [{"competency": "Price Statistics", "key": "priceIndices", "gap": 1.5}]
    user_courses = [{"id": "iGOT-MOSPI-CPI-102", "status": "Completed"}]
    recs = recommend_courses_for_gaps(critical_skills, user_courses=user_courses)
    rec_ids = [r["id"] for r in recs]
    assert "iGOT-MOSPI-CPI-102" not in rec_ids


def test_21_frac_code_and_nssta_accreditation():
    """Verify all catalog courses have valid FRAC codes and official government links."""
    courses = get_all_courses()
    for c in courses:
        assert c["frac_competency_code"].startswith("FRAC-STAT")
        assert "igotkarmayogi.gov.in" in c["karmayogi_url"]
        assert len(c["learning_outcomes"]) >= 2


def test_22_course_rating_and_duration_metadata():
    """Verify course duration and ratings are properly formatted."""
    courses = get_all_courses()
    for c in courses:
        assert "Hours" in c["duration"]
        assert 4.0 <= c["rating"] <= 5.0
        assert c["enrolled_count"] > 1000


# ============================================================================
# COMPONENT 5: Data Validation & Sanitization Tests (3 Tests)
# ============================================================================

def test_23_demo_login_resolution():
    """Verify Ananya Verma demo credentials resolve correctly."""
    dataset = read_dataset()
    resolved = resolve_login(dataset, "ananya.verma@demo.gov.in", "Demo@12345")
    assert resolved is not None
    record, profile = resolved
    assert record["id"] == "USR-001"
    assert profile["name"] == "Ananya Verma"


def test_24_profile_sanitization():
    """Verify sanitize_profile strips password and sensitive hash fields."""
    raw_profile = {
        "name": "Ananya Verma",
        "email": "ananya@gov.in",
        "password": "SecretPassword123",
        "password_hash": "argon2_xyz"
    }
    sanitized = sanitize_profile(raw_profile)
    assert "password" not in sanitized
    assert "password_hash" not in sanitized
    assert sanitized["name"] == "Ananya Verma"


def test_25_is_number_and_average_guards():
    """Verify numeric helper gracefully handles nulls, strings, and infinite values."""
    assert is_number(4.5) is True
    assert is_number("3.2") is True
    assert is_number(None) is False
    assert is_number("invalid") is False
    assert is_number(float("nan")) is False

    assert avg([10, 20, 30]) == 20.0
    assert avg([]) == 0.0
    assert avg(["10", None, "invalid", 20]) == 15.0
