from __future__ import annotations

import copy
import secrets
from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException

from api.deps import get_current_session
from repositories.dataset_repository import read_dataset, write_dataset
from schemas.auth_schemas import LoginRequest, RegisterRequest, UserUpdateRequest
from services.auth_service import (
    SESSIONS,
    build_user_payload,
    find_user_record,
    resolve_login,
    sanitize_profile,
)
from services.competency_service import ensure_competency_shape

router = APIRouter(tags=["Authentication & Users"])


@router.post("/api/auth/login")
def login(request: LoginRequest) -> dict[str, Any]:
    dataset = read_dataset()
    resolved = resolve_login(dataset, str(request.email), request.password)
    if not resolved:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    record, profile = resolved
    ensure_competency_shape(record)

    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {"id": record["id"], "profile": profile}

    return {
        "access_token": token,
        "token_type": "bearer",
        "data": build_user_payload(record, profile),
    }


@router.post("/api/auth/register")
def register(request: RegisterRequest) -> dict[str, Any]:
    dataset = read_dataset()
    existing = find_user_record(dataset, request.email)
    if existing is not None:
        raise HTTPException(
            status_code=400,
            detail="An account with this email address already exists.",
        )

    new_id = f"USR-{len(dataset.get('users', [])) + 1:03d}"
    is_general = request.account_type == "general"
    new_profile = {
        "name": request.name,
        "email": request.email,
        "password": request.password,
        "role": request.role,
        "department": request.department,
        "projectId": request.projectId,
        "accountType": "general" if is_general else "officer",
    }
    emp_code = (
        f"PUB-{secrets.randbelow(90000) + 10000}"
        if is_general
        else f"STAT-{secrets.randbelow(90000) + 10000}"
    )

    new_record = {
        "id": new_id,
        "employeeCode": emp_code,
        "profile": copy.deepcopy(new_profile),
        "dashboard": {
            "overallCompetency": 65 if is_general else 70,
            "overallCompetencyLabel": "65/100" if is_general else "70/100",
            "rank": "Citizen Scholar" if is_general else "A",
            "level": 65 if is_general else 70,
            "xp": 3000 if is_general else 4000,
            "completedModules": 0,
            "totalModules": 4,
            "learningProgress": 0,
            "criticalSkillGaps": 2,
            "moderateSkillGaps": 2,
            "strongSkills": 1,
            "assessmentAverage": 70,
            "learningHours": 10,
            "assessmentsCompleted": 0,
            "assessmentsTotal": 10,
            "assignmentsCompleted": 0,
            "assignmentsTotal": 1,
            "coursesCompleted": 0,
        },
        "competencies": [
            {"key": "statisticalMethods", "name": "Statistical Methods & Sampling", "score": 3.0, "scoreOutOf5": 3.0, "benchmark": 3.5, "level": "Moderate", "trend": "Stable", "weight": 1.15, "color": "cyan", "gap": 0.5},
            {"key": "nationalAccounts", "name": "National Accounts & Macroeconomics", "score": 2.5, "scoreOutOf5": 2.5, "benchmark": 3.5, "level": "Moderate", "trend": "Stable", "weight": 1.1, "color": "blue", "gap": 1.0},
            {"key": "priceIndices", "name": "Price Indices & Inflation", "score": 2.6, "scoreOutOf5": 2.6, "benchmark": 3.5, "level": "Moderate", "trend": "Stable", "weight": 1.05, "color": "amber", "gap": 0.9},
            {"key": "dataQuality", "name": "Data Quality & Survey Validation", "score": 3.0, "scoreOutOf5": 3.0, "benchmark": 3.5, "level": "Moderate", "trend": "Stable", "weight": 1.05, "color": "green", "gap": 0.5},
            {"key": "gis", "name": "GIS & Geospatial Demographics", "score": 2.8, "scoreOutOf5": 2.8, "benchmark": 3.0, "level": "Moderate", "trend": "Stable", "weight": 1.0, "color": "purple", "gap": 0.2},
            {"key": "python", "name": "Python & Automated Tabulation", "score": 3.5, "scoreOutOf5": 3.5, "benchmark": 3.0, "level": "Strong", "trend": "Improving", "weight": 1.0, "color": "green", "gap": 0.0},
            {"key": "machineLearning", "name": "Statistical Machine Learning & Predictive Analytics", "score": 2.0, "scoreOutOf5": 2.0, "benchmark": 3.0, "level": "Weak", "trend": "Stable", "weight": 0.95, "color": "red", "gap": 1.0},
        ],
        "criticalSkills": [
            {"competency": "Statistical Machine Learning & Predictive Analytics", "currentScore": 2.0, "benchmark": 3.0, "gap": 1.0, "priority": "High", "recommendedAction": "Enroll in foundational iGOT machine learning modules."},
            {"competency": "National Accounts & Macroeconomics", "currentScore": 2.5, "benchmark": 3.5, "gap": 1.0, "priority": "High", "recommendedAction": "Review SNA 2008 macroeconomics fundamentals."},
        ],
        "benchmarkComparison": [
            {"competency": "Statistical Methods", "currentScore": 3.0, "benchmark": 3.5, "status": "Requires Focus", "readinessPercent": 85.7},
            {"competency": "National Accounts", "currentScore": 2.5, "benchmark": 3.5, "status": "Requires Focus", "readinessPercent": 71.4},
            {"competency": "Price Statistics", "currentScore": 2.6, "benchmark": 3.5, "status": "Requires Focus", "readinessPercent": 74.2},
            {"competency": "Data Quality", "currentScore": 3.0, "benchmark": 3.5, "status": "Requires Focus", "readinessPercent": 85.7},
            {"competency": "GIS Analytics", "currentScore": 2.8, "benchmark": 3.0, "status": "Requires Focus", "readinessPercent": 93.3},
            {"competency": "Python for Statistics", "currentScore": 3.5, "benchmark": 3.0, "status": "Benchmark Met", "readinessPercent": 116.6},
            {"competency": "Machine Learning", "currentScore": 2.0, "benchmark": 3.0, "status": "Critical Gap", "readinessPercent": 66.6},
        ],
        "courses": [],
        "assignments": [],
        "documents": [],
        "certificates": [],
        "notifications": [
            {"id": "NOTIF-REG", "title": f"Welcome to StatSkill AI, {request.name}!", "time": "Just now", "color": "cyan"}
        ],
        "rawInputs": {
            "selfAssessment": {
                "statisticalMethods": [3.0, 3.0],
                "nationalAccounts": [2.5, 2.5],
                "priceIndices": [2.5, 2.5],
                "dataQuality": [3.0, 3.0],
                "gis": [2.8, 2.8],
                "python": [3.5, 3.5],
            },
            "learningHours": {
                "statisticalMethods": 4,
                "nationalAccounts": 2,
                "priceIndices": 2,
                "dataQuality": 2,
                "gis": 2,
                "python": 6,
            },
        },
        "learningPath": {
            "track": "Citizen Data Science & Open Statistics Learning Track" if is_general else "Official Statistical Cadre Capacity Track",
            "modulesCompleted": 0,
            "totalModules": 4,
            "modules": [
                {"step": 1, "title": "Foundations of National Statistical Datasets", "status": "In Progress", "state": "active", "duration": "8 hrs", "lessons": "0 / 6", "progress": 0},
                {"step": 2, "title": "Open Statistical Data Exploration & Python Analytics", "status": "Upcoming", "state": "locked", "duration": "10 hrs", "lessons": "0 / 8", "progress": 0},
                {"step": 3, "title": "Bhuvan Geospatial Visualizations for Demographics", "status": "Upcoming", "state": "locked", "duration": "8 hrs", "lessons": "0 / 7", "progress": 0},
                {"step": 4, "title": "Citizen Research Project & Capstone Assessment", "status": "Upcoming", "state": "locked", "duration": "6 hrs", "lessons": "0 / 3", "progress": 0},
            ],
        },
    }

    dataset.setdefault("users", []).append(new_record)
    write_dataset(dataset)

    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {"id": new_id, "profile": new_profile}

    return {
        "access_token": token,
        "token_type": "bearer",
        "data": build_user_payload(new_record, new_profile),
    }


@router.post("/api/auth/logout")
def logout(authorization: str | None = Header(default=None)) -> dict[str, bool]:
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ", 1)[1].strip()
        SESSIONS.pop(token, None)
    return {"ok": True}


@router.get("/api/me")
def me(session_data: tuple[dict[str, Any], dict[str, Any]] = Depends(get_current_session)) -> dict[str, Any]:
    record, profile = session_data
    payload = build_user_payload(record, profile)
    return {"user": payload["user"], "data": payload}


@router.get("/api/me/data")
def me_data(session_data: tuple[dict[str, Any], dict[str, Any]] = Depends(get_current_session)) -> dict[str, Any]:
    record, profile = session_data
    ensure_competency_shape(record)
    return build_user_payload(record, profile)


@router.put("/api/me/profile")
def update_profile(
    updates: UserUpdateRequest,
    session_data: tuple[dict[str, Any], dict[str, Any]] = Depends(get_current_session),
) -> dict[str, Any]:
    record, profile = session_data
    if updates.name and updates.name.strip():
        profile["name"] = updates.name.strip()
        record["profile"]["name"] = updates.name.strip()

    dataset = read_dataset()
    for idx, candidate in enumerate(dataset.get("users", [])):
        if candidate.get("id") == record.get("id"):
            dataset["users"][idx] = record
            break
    write_dataset(dataset)
    return build_user_payload(record, profile)


@router.get("/api/users/{email_or_id}/data")
def user_data(email_or_id: str) -> dict[str, Any]:
    dataset = read_dataset()
    record = find_user_record(dataset, email_or_id)
    if record is None:
        raise HTTPException(status_code=404, detail="User not found.")

    ensure_competency_shape(record)
    return build_user_payload(record, record.get("profile") or {})
