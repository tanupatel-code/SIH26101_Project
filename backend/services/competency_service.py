"""
Competency Service for StatSkill AI.
Implements multi-signal competency modeling, gap assessment, and dynamic reassessment
score updates for India's Official Statistical System.

Deterministic Pipeline:
Raw Evidence -> Calculated Score -> Optional Authorized Admin Override -> Final Published Score
-> Benchmark/Gap/Readiness -> Dashboard/Analytics
"""

from __future__ import annotations

import copy
import math
from typing import Any

ENGINE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "statisticalMethods": {
        "name": "Statistical Methods & Sampling",
        "benchmark": 3.5,
        "weight": 1.15,
        "subSkills": [
            "Sampling Design & Weights",
            "Hypothesis Testing & Inference",
            "Variance Estimation & Standard Errors",
            "Survey Stratification",
        ],
    },
    "nationalAccounts": {
        "name": "National Accounts (SNA & GDP)",
        "benchmark": 3.5,
        "weight": 1.10,
        "subSkills": [
            "GVA at Basic Prices",
            "GDP at Market Prices",
            "Supply & Use Tables (SUT)",
            "Institutional Sector Accounts",
        ],
    },
    "priceIndices": {
        "name": "Price Statistics (CPI/WPI/IIP)",
        "benchmark": 3.5,
        "weight": 1.05,
        "subSkills": [
            "CPI & WPI Compilation",
            "Modified Laspeyres Formula",
            "Inflation Deflators & Item Weights",
            "Index Quality Adjustment",
        ],
    },
    "dataQuality": {
        "name": "Data Quality & Survey Validation",
        "benchmark": 3.5,
        "weight": 1.05,
        "subSkills": [
            "Field Data Editing & Validation",
            "Hot-Deck & Cold-Deck Imputation",
            "Microdata Audit & Outlier Detection",
            "Data Quality Review & Standards",
        ],
    },
    "gis": {
        "name": "GIS & Spatial Statistics",
        "benchmark": 3.0,
        "weight": 1.0,
        "subSkills": [
            "Bhuvan & Geo-tagging",
            "Spatial Autocorrelation & Moran's I",
            "Choropleth Mapping",
            "Urban Frame Survey (UFS) Boundaries",
        ],
    },
    "python": {
        "name": "Python for Data Automation",
        "benchmark": 3.0,
        "weight": 1.0,
        "subSkills": [
            "Data Extraction & Cleaning",
            "pandas & numpy Tabulation",
            "Automated Reporting & Validation",
            "Statistical Script Optimization",
        ],
    },
    "machineLearning": {
        "name": "Machine Learning & AI",
        "benchmark": 3.0,
        "weight": 0.95,
        "subSkills": [
            "Supervised Learning for Official Statistics",
            "Time-Series Forecasting & Nowcasting",
            "Feature Engineering & Preprocessing",
            "Model Evaluation & Bias Auditing",
        ],
    },
}


def is_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def avg(values: list[Any]) -> float:
    nums = [float(v) for v in values if is_number(v)]
    return sum(nums) / len(nums) if nums else 0.0


def extract_domain_evidence(user_record: dict[str, Any], domain_key: str) -> dict[str, Any]:
    """Extracts raw evidence signals for a specific statistical domain."""
    raw_inputs = user_record.get("rawInputs")
    if not isinstance(raw_inputs, dict):
        raw_inputs = {}

    learning_hours_map = raw_inputs.get("learningHours")
    if not isinstance(learning_hours_map, dict):
        learning_hours_map = {}

    self_assessment_map = raw_inputs.get("selfAssessment")
    if not isinstance(self_assessment_map, dict):
        self_assessment_map = {}

    raw_history = user_record.get("assessmentHistory")
    assessment_history = [a for a in raw_history if isinstance(a, dict)] if isinstance(raw_history, list) else []

    raw_courses = user_record.get("courses")
    courses = [c for c in raw_courses if isinstance(c, dict)] if isinstance(raw_courses, list) else []

    # Domain assessment matching
    assessments = [
        a for a in assessment_history
        if str(a.get("domain", "")).lower() == domain_key.lower() or
        (domain_key == "statisticalMethods" and "sampling" in str(a.get("title", "")).lower()) or
        (domain_key == "nationalAccounts" and "national" in str(a.get("title", "")).lower()) or
        (domain_key == "priceIndices" and "price" in str(a.get("title", "")).lower())
    ]

    domain_courses = [
        c for c in courses
        if str(c.get("domain", "")).lower() == domain_key.lower()
    ]

    self_scores_raw = self_assessment_map.get(domain_key, [])
    self_scores = self_scores_raw if isinstance(self_scores_raw, list) else [self_scores_raw]
    lh_val = learning_hours_map.get(domain_key, 0)
    hours = float(lh_val or 0) if is_number(lh_val) else 0.0

    quiz_scores = [a.get("score") for a in assessments if is_number(a.get("score"))]
    course_scores = [c.get("score") for c in domain_courses if is_number(c.get("score"))]

    return {
        "assessments": assessments,
        "quizScores": quiz_scores,
        "quizAverage": avg(quiz_scores) if quiz_scores else None,
        "courses": domain_courses,
        "courseScores": course_scores,
        "courseAverage": avg(course_scores) if course_scores else None,
        "selfAssessment": self_scores,
        "selfAverage": avg(self_scores) if self_scores else None,
        "learningHours": hours,
    }


def has_domain_evidence(user_record: dict[str, Any], domain_key: str) -> bool:
    """Returns True if user has recorded assessments, courses, or effort for the domain."""
    evidence = extract_domain_evidence(user_record, domain_key)
    return bool(evidence["quizScores"] or evidence["courseScores"] or evidence["learningHours"] > 0)


def calculate_competency_scores(user_record: dict[str, Any]) -> dict[str, float]:
    """
    Computes domain competency scores from 4 multi-signal components:
    - Scored Quizzes & Assessments (50%)
    - Course Completions (25%)
    - Self-Assessment Ratings (15%)
    - Learning Effort & Hours (10%)
    Formula: score = quiz * 0.50 + course * 0.25 + self * 0.15 + effort * 0.10
    Bounded in [0.0, 5.0], rounded to 2 decimal places.
    """
    score_map: dict[str, float] = {}

    for key, definition in ENGINE_DEFINITIONS.items():
        ev = extract_domain_evidence(user_record, key)

        quiz = (ev["quizAverage"] / 20.0) if ev["quizAverage"] is not None else 2.5
        course = (ev["courseAverage"] / 20.0) if ev["courseAverage"] is not None else 2.5
        self_val = ev["selfAverage"] if ev["selfAverage"] is not None else 3.0
        effort = min(5.0, ev["learningHours"] / 8.0)

        # Multi-signal weighted formula
        score = quiz * 0.50 + course * 0.25 + self_val * 0.15 + effort * 0.10
        score_map[key] = round(max(0.0, min(5.0, score)), 2)

    return score_map


def ensure_competency_shape(user_record: dict[str, Any]) -> None:
    """
    Authoritative Competency Engine Pipeline:
    1. Raw Evidence: inspect quizzes, courses, self-assessment, and learning hours.
    2. Calculate Score: apply official 4-signal formula.
    3. Optional Authorized Admin Override: check user_record["adminOverrides"].
    4. Final Published Score: combine with source recording.
    5. Benchmarks, Gaps, Readiness, and Dashboard/Analytics derivation.
    """
    calculated = calculate_competency_scores(user_record)
    admin_overrides = user_record.get("adminOverrides")
    if not isinstance(admin_overrides, dict):
        admin_overrides = {}

    existing_scores = user_record.get("competencyScores")
    if not isinstance(existing_scores, dict):
        existing_scores = {}

    final_scores: dict[str, float] = {}
    sources: dict[str, str] = {}

    for key in ENGINE_DEFINITIONS:
        # Phase 3 Deterministic Flow:
        # 1. Highest precedence: Explicit Authorized Administrative Override
        if key in admin_overrides and is_number(admin_overrides[key]):
            final_scores[key] = float(admin_overrides[key])
            sources[key] = "admin_override"
        # 2. Evidence precedence: If new assessment or course evidence exists, calculated score applies!
        elif has_domain_evidence(user_record, key):
            final_scores[key] = calculated[key]
            sources[key] = "calculated_evidence"
        # 3. Seed / baseline score fallback if no evidence has been recorded yet
        elif key in existing_scores and is_number(existing_scores[key]):
            final_scores[key] = float(existing_scores[key])
            sources[key] = "baseline_score"
        else:
            final_scores[key] = calculated[key]
            sources[key] = "calculated_evidence"

    new_competencies: list[dict[str, Any]] = []
    for key, definition in ENGINE_DEFINITIONS.items():
        score = max(0.0, min(5.0, float(final_scores.get(key, 2.5))))
        benchmark = float(definition["benchmark"])
        gap = max(0.0, benchmark - score)
        level = "Strong" if score >= 3.5 else "Moderate" if score >= 2.0 else "Weak"

        ev = extract_domain_evidence(user_record, key)
        evidence_summary = {
            "quizAverage": round(ev["quizAverage"], 1) if ev["quizAverage"] is not None else None,
            "courseAverage": round(ev["courseAverage"], 1) if ev["courseAverage"] is not None else None,
            "selfAssessment": round(ev["selfAverage"], 1) if ev["selfAverage"] is not None else 3.0,
            "learningHours": ev["learningHours"],
        }

        new_competencies.append({
            "key": key,
            "name": definition["name"],
            "score": round(score, 2),
            "scoreOutOf5": round(score, 2),
            "scorePercent": round(score * 20, 1),
            "benchmark": benchmark,
            "gap": round(gap, 2),
            "gapPercent": round((gap / benchmark) * 100, 1) if benchmark else 0.0,
            "weight": float(definition["weight"]),
            "level": level,
            "source": sources.get(key, "calculated_evidence"),
            "evidence": evidence_summary,
            "subSkills": definition.get("subSkills", []),
        })

    user_record["competencies"] = new_competencies
    user_record["competencyScores"] = {str(item["key"]): float(item["score"]) for item in new_competencies}

    # Benchmark comparisons
    user_record["benchmarkComparison"] = [
        {
            "competency": item["name"],
            "key": item["key"],
            "currentScore": float(item["score"]),
            "benchmark": float(item["benchmark"]),
            "gap": float(item["gap"]),
            "status": "Benchmark Met" if float(item["gap"]) <= 0 else "Below Benchmark",
            "readinessPercent": round(min(100.0, (float(item["score"]) / float(item["benchmark"])) * 100), 1) if float(item["benchmark"]) else 0.0,
        }
        for item in new_competencies
    ]

    # Critical skill gaps (prioritized by highest gap)
    below = sorted(
        [item for item in new_competencies if float(item["gap"]) > 0],
        key=lambda item: float(item["gap"]),
        reverse=True,
    )
    user_record["criticalSkills"] = [
        {
            "competency": item["name"],
            "key": item["key"],
            "priority": "High" if float(item["gap"]) >= 1.0 else "Medium",
            "currentScore": float(item["score"]),
            "benchmark": float(item["benchmark"]),
            "gap": float(item["gap"]),
            "recommendedAction": f"Enroll in recommended iGOT Karmayogi modules to strengthen {item['name']}.",
        }
        for item in below
    ]

    # Overall dashboard score
    weighted_sum = sum(float(item["score"]) * float(item["weight"]) for item in new_competencies)
    total_weight = sum(float(item["weight"]) for item in new_competencies) or 1.0
    weighted_avg = weighted_sum / total_weight

    assessments = user_record.get("assessmentHistory") or []
    quiz_average = round(avg([a.get("score") for a in assessments])) if assessments else 70
    learning_hours_map = (user_record.get("rawInputs") or {}).get("learningHours") or {}
    total_hours = sum(float(v or 0) for v in learning_hours_map.values()) if isinstance(learning_hours_map, dict) else 0.0

    dashboard = user_record.setdefault("dashboard", {})
    overall_score = round(min(100, max(0, weighted_avg * 20 * 0.82 + quiz_average * 0.12 + min(total_hours, 100) * 0.06)))
    dashboard["overallCompetency"] = overall_score
    dashboard["overallCompetencyLabel"] = f"{overall_score}/100"
    dashboard["criticalSkillGaps"] = sum(1 for item in user_record["criticalSkills"] if str(item.get("priority")) == "High")
    dashboard["moderateSkillGaps"] = sum(1 for item in new_competencies if float(item["gap"]) > 0 and str(item.get("level")) != "Weak")
    dashboard["strongSkills"] = sum(1 for item in new_competencies if str(item.get("level")) == "Strong")
    dashboard["assessmentsCompleted"] = len(assessments)

    user_record["analytics"] = {
        **(user_record.get("analytics") or {}),
        "competencyScores": dict(user_record["competencyScores"]),
        "totalLearningHours": total_hours,
        "quizAverage": quiz_average,
    }


def record_quiz_submission(
    user_record: dict[str, Any],
    quiz_title: str,
    domain: str,
    score_percentage: float,
    answers_detail: list[dict[str, Any]]
) -> dict[str, Any]:
    """
    Records a completed quiz attempt and immediately recalculates the officer's
    competency scores, skill gaps, and learning recommendations.
    """
    assessment_history = user_record.setdefault("assessmentHistory", [])
    new_assessment = {
        "id": f"ASM-{len(assessment_history) + 1:03d}",
        "title": quiz_title,
        "domain": domain,
        "score": round(score_percentage, 1),
        "date": "Just now",
        "status": "Completed",
        "details": answers_detail,
    }
    assessment_history.append(new_assessment)

    # Re-evaluate all competencies and update profile based on new evidence
    ensure_competency_shape(user_record)

    return {
        "assessment": new_assessment,
        "updatedCompetency": user_record.get("competencyScores", {}).get(domain),
        "overallCompetency": user_record.get("dashboard", {}).get("overallCompetency"),
    }
