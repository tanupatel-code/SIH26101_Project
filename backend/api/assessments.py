from typing import Any
from fastapi import APIRouter, Header, HTTPException

from repositories.dataset_repository import read_dataset, write_dataset
from schemas.assessment_schemas import McqGenerateRequest, QuizSubmitRequest
from services.assessment_service import (
    grade_submission,
    record_quiz_submission,
    register_generated_questions,
)
from services.auth_service import build_user_payload, session_record
from services.mcq_generator import generate_mcqs_from_text

router = APIRouter(tags=["assessments"])


@router.post("/api/mcq/generate")
def generate_mcqs(
    request: McqGenerateRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """
    Generates AI Quizzes / MCQs from an uploaded document, provided text, or a specific statistical topic.
    """
    text_to_process = ""

    if request.document_id and authorization:
        record, _ = session_record(authorization)
        for doc in record.get("documents", []):
            if doc.get("id") == request.document_id:
                text_to_process = doc.get("extractedText", "")
                break

    if not text_to_process:
        text_to_process = request.document_text or request.topic or ""

    questions = generate_mcqs_from_text(
        text=text_to_process,
        num_questions=request.num_questions,
        difficulty=request.difficulty,
        bloom_level=request.bloom_level,
        target_domain=request.domain,
    )

    # Register authoritative answer keys server-side
    register_generated_questions(questions)

    return {
        "ok": True,
        "questionCount": len(questions),
        "difficulty": request.difficulty,
        "bloomLevel": request.bloom_level,
        "domain": request.domain or "General Statistics",
        "questions": questions,
    }


@router.get("/api/assessments/available")
def get_available_assessments() -> dict[str, Any]:
    """
    Returns available official statistical diagnostic quizzes that officers can take.
    """
    quizzes = [
        {
            "id": "QUIZ-SAMPLING",
            "title": "National Sample Survey Sampling & Estimation Diagnostic",
            "domain": "statisticalMethods",
            "domainName": "Statistical Methods & Sampling",
            "duration": "15 Mins",
            "questionCount": 5,
            "difficulty": "Intermediate",
            "description": "Evaluate proficiency in stratified multi-stage designs, sampling weights, and variance estimation.",
        },
        {
            "id": "QUIZ-SNA",
            "title": "System of National Accounts (SNA 2008) & GDP Diagnostic",
            "domain": "nationalAccounts",
            "domainName": "National Accounts (SNA & GDP)",
            "duration": "15 Mins",
            "questionCount": 5,
            "difficulty": "Advanced",
            "description": "Assess understanding of GVA vs GDP, product taxes/subsidies, and institutional sector accounts.",
        },
        {
            "id": "QUIZ-CPI",
            "title": "Consumer Price Index (CPI) Compilation & Inflation Deflators",
            "domain": "priceIndices",
            "domainName": "Price Statistics (CPI/WPI/IIP)",
            "duration": "12 Mins",
            "questionCount": 5,
            "difficulty": "Intermediate",
            "description": "Test competencies in price quotation audits, Laspeyres weighting, and seasonal adjustments.",
        },
        {
            "id": "QUIZ-DQ",
            "title": "Survey Data Editing, Validation & Hot-Deck Imputation",
            "domain": "dataQuality",
            "domainName": "Data Quality & Survey Validation",
            "duration": "12 Mins",
            "questionCount": 5,
            "difficulty": "Intermediate",
            "description": "Measure ability to validate survey records, execute range checks, and audit microdata.",
        },
        {
            "id": "QUIZ-GIS",
            "title": "Spatial Statistics & Geo-Tagging in Official Surveys",
            "domain": "gis",
            "domainName": "GIS & Spatial Statistics",
            "duration": "15 Mins",
            "questionCount": 5,
            "difficulty": "Advanced",
            "description": "Examine skills in spatial autocorrelation, Moran's I, and thematic choropleth generation.",
        },
        {
            "id": "QUIZ-PYTHON",
            "title": "Python Data Automation for Official Statistics",
            "domain": "python",
            "domainName": "Python for Data Automation",
            "duration": "15 Mins",
            "questionCount": 5,
            "difficulty": "Intermediate",
            "description": "Assess proficiency in automated data transformations, pandas aggregations, and script validation.",
        },
    ]
    return {"quizzes": quizzes}


@router.post("/api/assessments/submit")
def submit_assessment(
    request: QuizSubmitRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """
    Submits completed assessment responses, grades them instantly,
    and dynamically recalculates the officer's competency profile, skill gaps,
    and dashboard readiness!
    """
    record, profile = session_record(authorization)
    if not request.answers:
        raise HTTPException(status_code=400, detail="No answers provided in quiz submission.")

    # Server authoritatively grades answers against authoritative question bank
    correct, total, percentage, answers_detail = grade_submission(
        request.quiz_id, request.answers
    )

    result = record_quiz_submission(
        user_record=record,
        quiz_title=request.title,
        domain=request.domain,
        score_percentage=percentage,
        answers_detail=answers_detail,
    )

    # Persist updated user record in statskill.json
    dataset = read_dataset()
    for idx, candidate in enumerate(dataset.get("users", [])):
        if candidate.get("id") == record.get("id"):
            dataset["users"][idx] = record
            break
    write_dataset(dataset)

    return {
        "ok": True,
        "quizId": request.quiz_id,
        "score": percentage,
        "correctCount": correct,
        "totalQuestions": total,
        "domain": request.domain,
        "updatedCompetencyScore": result["updatedCompetency"],
        "overallCompetency": result["overallCompetency"],
        "userPayload": build_user_payload(record, profile),
    }
