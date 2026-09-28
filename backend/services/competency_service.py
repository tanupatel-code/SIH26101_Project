"""
Competency Service for StatSkill AI.
Implements multi-signal competency modeling, gap assessment, and dynamic reassessment
score updates for India's Official Statistical System.
"""

from __future__ import annotations

import copy
import math
from typing import Any

ENGINE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "statisticalMethods": {"name": "Statistical Methods & Sampling", "benchmark": 3.5, "weight": 1.15},
    "nationalAccounts": {"name": "National Accounts (SNA & GDP)", "benchmark": 3.5, "weight": 1.10},
    "priceIndices": {"name": "Price Statistics (CPI/WPI/IIP)", "benchmark": 3.5, "weight": 1.05},
    "dataQuality": {"name": "Data Quality & Survey Validation", "benchmark": 3.5, "weight": 1.05},
    "gis": {"name": "GIS & Spatial Statistics", "benchmark": 3.0, "weight": 1.0},
    "python": {"name": "Python for Data Automation", "benchmark": 3.0, "weight": 1.0},
    "machineLearning": {"name": "Machine Learning & AI", "benchmark": 3.0, "weight": 0.95},
}


def is_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def avg(values: list[Any]) -> float:
    nums = [float(v) for v in values if is_number(v)]
    return sum(nums) / len(nums) if nums else 0.0


def calculate_competency_scores(user_record: dict[str, Any]) -> dict[str, float]:
    """
    Computes domain competency scores from 4 multi-signal components:
    - Scored Quizzes & Assessments (50%)
    - Course Completions (25%)
    - Self-Assessment Ratings (15%)
    - Learning Effort & Hours (10%)
    """
    raw_inputs = user_record.get("rawInputs")
    if not isinstance(raw_inputs, dict):
        raw_inputs = {}

    learning_hours = raw_inputs.get("learningHours")
    if not isinstance(learning_hours, dict):
        learning_hours = {}

    self_assessment = raw_inputs.get("selfAssessment")
    if not isinstance(self_assessment, dict):
        self_assessment = {}

    raw_history = user_record.get("assessmentHistory")
    assessment_history = [a for a in raw_history if isinstance(a, dict)] if isinstance(raw_history, list) else []

    raw_courses = user_record.get("courses")
    courses = [c for c in raw_courses if isinstance(c, dict)] if isinstance(raw_courses, list) else []

    score_map: dict[str, float] = {}

    for key, definition in ENGINE_DEFINITIONS.items():
        # Filter assessments and courses belonging to this domain
        assessments = [
            a for a in assessment_history
            if str(a.get("domain", "")).lower() == key.lower() or
            (key == "statisticalMethods" and "sampling" in str(a.get("title", "")).lower()) or
            (key == "nationalAccounts" and "national" in str(a.get("title", "")).lower()) or
            (key == "priceIndices" and "price" in str(a.get("title", "")).lower())
        ]
        domain_courses = [
            c for c in courses
            if str(c.get("domain", "")).lower() == key.lower()
        ]

        quiz_scores = [a.get("score") for a in assessments if is_number(a.get("score"))]
        course_scores = [c.get("score") for c in domain_courses if is_number(c.get("score"))]
        self_scores_raw = self_assessment.get(key, [])
        self_scores = self_scores_raw if isinstance(self_scores_raw, list) else [self_scores_raw]

        quiz = (avg(quiz_scores) / 20.0) if quiz_scores else 2.5
        course = (avg(course_scores) / 20.0) if course_scores else 2.5
        self_val = avg(self_scores) if self_scores else 3.0
        lh_val = learning_hours.get(key, 0)
        effort = min(5.0, float(lh_val or 0) / 8.0) if is_number(lh_val) else 0.0

        # Multi-signal weighted formula
        score = quiz * 0.50 + course * 0.25 + self_val * 0.15 + effort * 0.10
        score_map[key] = round(max(0.0, min(5.0, score)), 2)

    return score_map


def ensure_competency_shape(user_record: dict[str, Any]) -> None:
    """
    Synchronizes derived competency structures across the user profile:
    - competencies array with benchmark, gap, readiness, level
    - criticalSkills list prioritized by gap
    - benchmarkComparison items
    - overall dashboard competency score
    - analytics and engine metrics
    """
    # Recalculate dynamic scores based on assessment history and courses
    calculated = calculate_competency_scores(user_record)
    existing_scores = user_record.get("competencyScores") or {}
    
    # Merge authoritative explicit scores if provided
    final_scores = {}
    for k, v in calculated.items():
        if k in existing_scores and is_number(existing_scores[k]):
            # If user had an explicit override, take it, otherwise calculated
            final_scores[k] = float(existing_scores[k])
        else:
            final_scores[k] = v

    new_competencies: list[dict[str, Any]] = []
    for key, definition in ENGINE_DEFINITIONS.items():
        score = max(0.0, min(5.0, float(final_scores.get(key, 2.5))))
        benchmark = float(definition["benchmark"])
        gap = max(0.0, benchmark - score)
        level = "Strong" if score >= 3.5 else "Moderate" if score >= 2.0 else "Weak"

        new_competencies.append({
            "key": key,
            "name": definition["name"],
            "score": round(score, 2),
            "scoreOutOf5": round(score, 2),
            "scorePercent": round(score * 20, 1),
            "benchmark": benchmark,
            "gap": round(gap, 2),
            "gapPercent": round((gap / benchmark) * 100, 1) if benchmark else 0,
            "weight": float(definition["weight"]),
            "level": level,
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
            "readinessPercent": round(min(100, (float(item["score"]) / float(item["benchmark"])) * 100), 1) if float(item["benchmark"]) else 0,
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
    total_hours = sum(float(v or 0) for v in learning_hours_map.values())

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

    # Re-evaluate all competencies and update profile
    ensure_competency_shape(user_record)

    return {
        "assessment": new_assessment,
        "updatedCompetency": user_record.get("competencyScores", {}).get(domain),
        "overallCompetency": user_record.get("dashboard", {}).get("overallCompetency"),
    }
