from typing import Any
from fastapi import APIRouter, Header, HTTPException

from repositories.dataset_repository import read_dataset, write_dataset
from schemas.admin_schemas import EnrollRequest
from services.auth_service import build_user_payload, session_record
from services.competency_service import ensure_competency_shape
from services.igot_service import (
    IGOT_COURSE_CATALOG,
    get_all_courses,
    recommend_courses_for_gaps,
)

router = APIRouter(tags=["igot"])


@router.get("/api/igot/courses")
def igot_courses(
    domain: str | None = None,
    level: str | None = None,
) -> dict[str, Any]:
    """Returns the official iGOT Karmayogi course catalog for India's Official Statistical System."""
    courses = get_all_courses(domain=domain, level=level)
    return {"courses": courses, "total": len(courses)}


@router.get("/api/igot/recommendations")
def igot_recommendations(
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """
    Returns personalized iGOT Karmayogi course recommendations
    tailored specifically to bridge the logged-in officer's diagnosed competency gaps.
    """
    record, _ = session_record(authorization)
    critical_skills = record.get("criticalSkills") or []
    user_courses = record.get("courses") or []
    recommendations = recommend_courses_for_gaps(critical_skills, user_courses)

    return {
        "recommendations": recommendations,
        "gapCount": len(critical_skills),
        "topGap": critical_skills[0].get("competency") if critical_skills else None,
    }


@router.post("/api/igot/enroll")
def igot_enroll(
    request: EnrollRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """
    Enrolls the officer into an iGOT Karmayogi training module,
    dynamically updates their active courses, logs learning hours, and updates their profile.
    """
    record, profile = session_record(authorization)
    catalog = {c["id"]: c for c in IGOT_COURSE_CATALOG}
    course_meta = catalog.get(request.course_id)
    if not course_meta:
        raise HTTPException(status_code=404, detail="iGOT Course not found.")

    courses = record.setdefault("courses", [])
    existing = next((c for c in courses if c.get("id") == request.course_id), None)
    if not existing:
        course_entry = {
            "id": course_meta["id"],
            "title": course_meta["title"],
            "domain": course_meta["competency_domain"],
            "score": 0,
            "progress": 15,
            "hours": 4,
            "status": "In Progress",
            "provider": course_meta["provider"],
            "karmayogiUrl": course_meta["karmayogi_url"],
        }
        courses.insert(0, course_entry)

        # Log learning hours
        raw_inputs = record.setdefault("rawInputs", {})
        hours_map = raw_inputs.setdefault("learningHours", {})
        dom = course_meta["competency_domain"]
        hours_map[dom] = float(hours_map.get(dom, 0)) + 4.0

        # Recalculate competency shape
        ensure_competency_shape(record)

        # Persist in dataset
        dataset = read_dataset()
        for idx, candidate in enumerate(dataset.get("users", [])):
            if candidate.get("id") == record.get("id"):
                dataset["users"][idx] = record
                break
        write_dataset(dataset)

    return {
        "ok": True,
        "enrolledCourse": course_meta,
        "userPayload": build_user_payload(record, profile),
    }
