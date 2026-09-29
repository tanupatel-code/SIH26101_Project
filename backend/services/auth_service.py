from __future__ import annotations

import copy
import secrets
from typing import Any
from fastapi import HTTPException

from repositories.dataset_repository import read_demo, write_dataset
from services.competency_service import (
    ensure_competency_shape,
    ENGINE_DEFINITIONS,
)
from services.igot_service import (
    recommend_courses_for_gaps,
    IGOT_COURSE_CATALOG,
)

# Active user sessions mapped by bearer token
SESSIONS: dict[str, dict[str, Any]] = {}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def sanitize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in profile.items()
        if str(key).lower() not in {"password", "password_hash"}
    }


def find_user_record(dataset: dict[str, Any], email_or_id: str) -> dict[str, Any] | None:
    target = email_or_id.strip().lower()
    for record in dataset.get("users", []):
        profile = record.get("profile") or {}
        candidates = [
            str(record.get("id", "")),
            str(record.get("employeeCode", "")),
            str(profile.get("email", "")),
        ]
        if any(target == candidate.lower() for candidate in candidates):
            return record

    return None


def create_user_from_demo_profile(demo_user: dict[str, Any]) -> dict[str, Any]:
    user_id = str(demo_user.get("id") or f"USR-{secrets.token_hex(3).upper()}")
    is_general = demo_user.get("accountType") == "general"
    emp_code = (
        f"PUB-{secrets.randbelow(90000) + 10000}"
        if is_general
        else f"STAT-{secrets.randbelow(90000) + 10000}"
    )
    name = str(demo_user.get("name", "Statistical Learner"))
    record: dict[str, Any] = {
        "id": user_id,
        "employeeCode": emp_code,
        "profile": copy.deepcopy(demo_user),
        "dashboard": {
            "overallCompetency": 68 if is_general else 72,
            "overallCompetencyLabel": "68/100" if is_general else "72/100",
            "rank": "Citizen Scholar" if is_general else "A",
            "level": 68 if is_general else 72,
            "xp": 3400 if is_general else 4850,
            "completedModules": 1,
            "totalModules": 4,
            "learningProgress": 25,
            "criticalSkillGaps": 2,
            "moderateSkillGaps": 1,
            "strongSkills": 2,
            "assessmentAverage": 74 if is_general else 78,
            "learningHours": 32 if is_general else 48,
            "assessmentsCompleted": 10,
            "assessmentsTotal": 10,
            "assignmentsCompleted": 1,
            "assignmentsTotal": 1,
            "coursesCompleted": 4,
        },
        "competencies": [
            {
                "key": "statisticalMethods",
                "name": "Statistical Methods & Sampling",
                "score": 3.7 if not is_general else 3.4,
                "scoreOutOf5": 3.7 if not is_general else 3.4,
                "benchmark": 3.5,
                "level": "Strong" if not is_general else "Moderate",
                "trend": "Improving",
                "weight": 1.15,
                "color": "cyan",
                "gap": 0.0 if not is_general else 0.1,
            },
            {
                "key": "nationalAccounts",
                "name": "National Accounts & Macroeconomics",
                "score": 2.8 if not is_general else 2.4,
                "scoreOutOf5": 2.8 if not is_general else 2.4,
                "benchmark": 3.5,
                "level": "Moderate",
                "trend": "Stable",
                "weight": 1.1,
                "color": "blue",
                "gap": 0.7 if not is_general else 1.1,
            },
            {
                "key": "priceIndices",
                "name": "Price Indices & Inflation",
                "score": 2.9 if not is_general else 2.6,
                "scoreOutOf5": 2.9 if not is_general else 2.6,
                "benchmark": 3.5,
                "level": "Moderate",
                "trend": "Stable",
                "weight": 1.05,
                "color": "amber",
                "gap": 0.6 if not is_general else 0.9,
            },
            {
                "key": "dataQuality",
                "name": "Data Quality & Survey Validation",
                "score": 3.6 if not is_general else 3.2,
                "scoreOutOf5": 3.6 if not is_general else 3.2,
                "benchmark": 3.5,
                "level": "Strong" if not is_general else "Moderate",
                "trend": "Improving",
                "weight": 1.05,
                "color": "green",
                "gap": 0.0 if not is_general else 0.3,
            },
            {
                "key": "gis",
                "name": "GIS & Geospatial Demographics",
                "score": 2.9 if not is_general else 2.8,
                "scoreOutOf5": 2.9 if not is_general else 2.8,
                "benchmark": 3.0,
                "level": "Moderate",
                "trend": "Stable",
                "weight": 1.0,
                "color": "purple",
                "gap": 0.1 if not is_general else 0.2,
            },
            {
                "key": "python",
                "name": "Python & Automated Tabulation",
                "score": 3.8 if not is_general else 4.2,
                "scoreOutOf5": 3.8 if not is_general else 4.2,
                "benchmark": 3.0,
                "level": "Strong",
                "trend": "Improving",
                "weight": 1.0,
                "color": "green",
                "gap": 0.0,
            },
            {
                "key": "machineLearning",
                "name": "Statistical Machine Learning & Predictive Analytics",
                "score": 2.1 if not is_general else 2.4,
                "scoreOutOf5": 2.1 if not is_general else 2.4,
                "benchmark": 3.0,
                "level": "Weak",
                "trend": "Declining",
                "weight": 0.95,
                "color": "red",
                "gap": 0.9 if not is_general else 0.6,
            },
        ],
        "criticalSkills": [
            {
                "competency": "Statistical Machine Learning & Predictive Analytics",
                "currentScore": 2.1 if not is_general else 2.4,
                "benchmark": 3.0,
                "gap": 0.9 if not is_general else 0.6,
                "priority": "High",
                "recommendedAction": "Enroll in iGOT Course 'Supervised Machine Learning for Survey Imputation & Forecasting'.",
            },
            {
                "competency": "National Accounts & Macroeconomics",
                "currentScore": 2.8 if not is_general else 2.4,
                "benchmark": 3.5,
                "gap": 0.7 if not is_general else 1.1,
                "priority": "Medium",
                "recommendedAction": "Study CSO guidelines on SNA 2008 and GDP compilation methodology.",
            },
        ],
        "benchmarkComparison": [
            {"competency": "Statistical Methods", "currentScore": 3.7, "benchmark": 3.5, "status": "Benchmark Met", "readinessPercent": 105.7},
            {"competency": "National Accounts", "currentScore": 2.8, "benchmark": 3.5, "status": "Requires Focus", "readinessPercent": 80.0},
            {"competency": "Price Statistics", "currentScore": 2.9, "benchmark": 3.5, "status": "Requires Focus", "readinessPercent": 82.8},
            {"competency": "Data Quality", "currentScore": 3.6, "benchmark": 3.5, "status": "Benchmark Met", "readinessPercent": 102.8},
            {"competency": "GIS Analytics", "currentScore": 2.9, "benchmark": 3.0, "status": "Requires Focus", "readinessPercent": 96.6},
            {"competency": "Python for Statistics", "currentScore": 3.8, "benchmark": 3.0, "status": "Benchmark Met", "readinessPercent": 126.6},
            {"competency": "Machine Learning", "currentScore": 2.1, "benchmark": 3.0, "status": "Critical Gap", "readinessPercent": 70.0},
        ],
        "courses": [],
        "assignments": [
            {
                "id": "ASG-001",
                "title": "NSSO Round 78 Sampling Weight Calibration",
                "domain": "statisticalMethods",
                "score": 88,
                "maxScore": 100,
                "attempt": 1,
                "status": "Completed",
                "date": "2026-08-28",
            },
        ],
        "documents": [],
        "certificates": [],
        "notifications": [
            {
                "id": "NOTIF-01",
                "title": f"Welcome to StatSkill AI, {name}!",
                "time": "Just now",
                "color": "cyan",
            }
        ],
        "rawInputs": {
            "selfAssessment": {
                "statisticalMethods": [3.4, 3.4],
                "nationalAccounts": [2.4, 2.4],
                "priceIndices": [2.6, 2.6],
                "dataQuality": [3.2, 3.2],
                "gis": [2.8, 2.8],
                "python": [4.2, 4.2],
            },
            "learningHours": {
                "statisticalMethods": 12,
                "nationalAccounts": 4,
                "priceIndices": 4,
                "dataQuality": 8,
                "gis": 6,
                "python": 14,
            },
        },
        "learningPath": {
            "track": (
                "Citizen Data Science & Open Statistics Learning Track"
                if is_general
                else "Official Statistical Cadre Capacity Track"
            ),
            "modulesCompleted": 1,
            "totalModules": 4,
            "modules": [
                {"step": 1, "title": "Foundations of National Statistical Datasets", "status": "Completed", "state": "done", "duration": "8 hrs", "lessons": "6 / 6", "progress": 100},
                {"step": 2, "title": "Open Statistical Data Exploration & Python Analytics", "status": "In Progress", "state": "active", "duration": "10 hrs", "lessons": "4 / 8", "progress": 42},
                {"step": 3, "title": "Bhuvan Geospatial Visualizations for Demographics", "status": "Upcoming", "state": "locked", "duration": "8 hrs", "lessons": "0 / 7", "progress": 0},
                {"step": 4, "title": "Citizen Research Project & Capstone Assessment", "status": "Upcoming", "state": "locked", "duration": "6 hrs", "lessons": "0 / 3", "progress": 0},
            ],
        },
    }
    return record


def resolve_login(
    dataset: dict[str, Any], email: str, password: str
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    target_email = email.strip().lower()
    for record in dataset.get("users", []):
        profile = record.get("profile") or {}
        if str(profile.get("email", "")).strip().lower() == target_email:
            stored_pw = str(profile.get("password", ""))
            if secrets.compare_digest(stored_pw, password) or secrets.compare_digest(
                stored_pw.strip(), password.strip()
            ):
                return record, profile

    demo = read_demo()
    for demo_key in ("user", "public_user"):
        demo_user = demo.get(demo_key)
        if isinstance(demo_user, dict):
            if str(demo_user.get("email", "")).strip().lower() == target_email:
                stored_pw = str(demo_user.get("password", ""))
                if secrets.compare_digest(
                    stored_pw, password
                ) or secrets.compare_digest(stored_pw.strip(), password.strip()):
                    record = find_user_record(dataset, target_email)
                    if record is None:
                        record = create_user_from_demo_profile(demo_user)
                        dataset.setdefault("users", []).append(record)
                        write_dataset(dataset)
                    merged_profile = deep_merge(
                        record.get("profile") or {}, demo_user
                    )
                    return record, merged_profile

    return None


def build_user_payload(
    record: dict[str, Any], effective_profile: dict[str, Any] | None = None
) -> dict[str, Any]:
    record = copy.deepcopy(record)
    profile = sanitize_profile(effective_profile or record.get("profile") or {})
    user = {
        "id": record.get("id"),
        "employeeCode": record.get("employeeCode"),
        **profile,
    }

    modules = (record.get("learningPath") or {}).get("modules") or []
    competencies = record.get("competencies") or []
    competency_scores = {
        str(item.get("key")): item.get("score")
        for item in competencies
        if isinstance(item, dict) and item.get("key") and item.get("score") is not None
    }

    critical_skills = record.get("criticalSkills") or []
    user_courses = record.get("courses") or []
    igot_recommendations = recommend_courses_for_gaps(critical_skills, user_courses)

    return {
        "user": user,
        "id": record.get("id"),
        "employeeCode": record.get("employeeCode"),
        "profile": profile,
        "dashboard": record.get("dashboard") or {},
        "competencyScores": competency_scores or record.get("competencyScores") or {},
        "competencies": competencies,
        "criticalSkills": critical_skills,
        "benchmarkComparison": record.get("benchmarkComparison") or [],
        "learningPath": record.get("learningPath") or {},
        "modules": modules,
        "courses": record.get("courses") or [],
        "assignments": record.get("assignments") or [],
        "assessmentHistory": record.get("assessmentHistory") or [],
        "assessments": record.get("assessmentHistory") or [],
        "documents": record.get("documents") or [],
        "certificates": record.get("certificates") or [],
        "notifications": record.get("notifications") or [],
        "analytics": record.get("analytics") or {},
        "engine": record.get("engine") or {},
        "rawInputs": record.get("rawInputs") or {},
        "selfAssessment": (record.get("rawInputs") or {}).get("selfAssessment") or {},
        "learningHours": (record.get("rawInputs") or {}).get("learningHours") or {},
        "igotRecommendations": igot_recommendations,
        "igot_recommendations": igot_recommendations,
        "summary": {
            "dashboard": record.get("dashboard") or {},
            "competencies": competencies,
            "criticalSkills": critical_skills,
            "benchmarkComparison": record.get("benchmarkComparison") or [],
            "analytics": record.get("analytics") or {},
            "engine": record.get("engine") or {},
        },
    }


def session_record(authorization: str | None) -> tuple[dict[str, Any], dict[str, Any]]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token.")
    token = authorization.split(" ", 1)[1].strip()
    session = SESSIONS.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session.")

    from repositories.dataset_repository import read_dataset
    dataset = read_dataset()
    record = find_user_record(dataset, session["id"])
    if not record:
        raise HTTPException(status_code=401, detail="Session user no longer exists.")

    return record, session.get("profile") or record.get("profile") or {}
