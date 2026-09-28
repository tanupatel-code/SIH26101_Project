from __future__ import annotations

import copy
import json
import math
import os
import secrets
import sys
from pathlib import Path
from threading import Lock
from typing import Any

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, EmailStr, Field

# Ensure local services can be imported regardless of execution working directory
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from services.document_parser import extract_document_text, chunk_document
from services.mcq_generator import generate_mcqs_from_text, OFFICIAL_STATS_CONCEPTS
from services.igot_service import (
    get_all_courses,
    recommend_courses_for_gaps,
    IGOT_COURSE_CATALOG,
)
from services.competency_service import (
    ENGINE_DEFINITIONS,
    calculate_competency_scores,
    ensure_competency_shape,
    record_quiz_submission,
)

DATA_FILE = Path(os.getenv("STATSKILL_DATA_FILE", BASE_DIR / "statskill.json"))
DEMO_FILE = Path(os.getenv("STATSKILL_DEMO_FILE", BASE_DIR / "demo.json"))
DATA_SOURCES_FILE = Path(os.getenv("STATSKILL_DATA_SOURCES_FILE", BASE_DIR / "data_sources.json"))
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ADMIN_KEY = os.getenv("STATSKILL_ADMIN_KEY", "dev-admin-key")
DATA_LOCK = Lock()
SESSIONS: dict[str, dict[str, Any]] = {}

app = FastAPI(
    title="StatSkill AI — Official Statistical Learning & Competency API",
    version="3.0.0",
    description=(
        "AI-enabled competency intelligence and capacity building platform for "
        "India's Official Statistical System (MoSPI/NSSTA) with iGOT Karmayogi integration."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "STATSKILL_CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Pydantic Request Models
# ==========================================

class LoginRequest(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=1)


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)
    password: str = Field(min_length=6)
    role: str = "Statistical Investigator"
    department: str = "MoSPI"
    projectId: str = "SIH26101"
    account_type: str = "officer"


class UserUpdateRequest(BaseModel):
    name: str | None = None


class AdminUserPatch(BaseModel):
    data: dict[str, Any]


class AdminDatasetUpdate(BaseModel):
    data: dict[str, Any]


class McqGenerateRequest(BaseModel):
    document_id: str | None = None
    document_text: str | None = None
    topic: str | None = None
    num_questions: int = Field(default=5, ge=1, le=20)
    difficulty: str = Field(default="Intermediate")
    bloom_level: str = Field(default="Understanding")
    domain: str | None = None


class QuizAnswerItem(BaseModel):
    question_id: str
    selected_option: int
    correct_option: int
    is_correct: bool


class QuizSubmitRequest(BaseModel):
    quiz_id: str = "QUIZ-GENERAL"
    title: str = "Statistical Competency Quiz"
    domain: str = "statisticalMethods"
    answers: list[QuizAnswerItem]


class EnrollRequest(BaseModel):
    course_id: str


# ==========================================
# Storage Helpers
# ==========================================

def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise HTTPException(status_code=500, detail=f"Data file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_dataset() -> dict[str, Any]:
    with DATA_LOCK:
        return read_json(DATA_FILE)


def read_demo() -> dict[str, Any]:
    with DATA_LOCK:
        return read_json(DEMO_FILE)


def write_dataset(data: dict[str, Any]) -> None:
    with DATA_LOCK:
        write_json(DATA_FILE, data)


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in patch.items():
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
    emp_code = f"PUB-{secrets.randbelow(90000) + 10000}" if is_general else f"STAT-{secrets.randbelow(90000) + 10000}"
    name = str(demo_user.get("name", "Statistical Learner"))
    record: dict[str, Any] = {
        "id": user_id,
        "employeeCode": emp_code,
        "profile": copy.deepcopy(demo_user),
        "dashboard": {
            "overallCompetency": 68 if is_general else 72,
            "overallCompetencyLabel": "68/100" if is_general else "72/100",
            "rank": "Citizen Scholar" if is_general else "A",
            "level": 64,
            "xp": 3200,
            "criticalSkillGaps": 2,
            "moderateSkillGaps": 3,
            "strongSkills": 2,
            "assessmentsCompleted": 4 if is_general else 23,
            "learningProgress": 42 if is_general else 35,
            "completedModules": 1,
            "totalModules": 4,
            "learningHours": 48 if is_general else 150,
            "activeModule": "Open Statistical Data Exploration & Python Analytics" if is_general else "GIS & Spatial Statistics Intermediate Practice",
        },
        "competencyScores": {
            "statisticalMethods": 3.4 if is_general else 4.8,
            "nationalAccounts": 2.4 if is_general else 3.5,
            "priceIndices": 2.6 if is_general else 2.3,
            "dataQuality": 3.2 if is_general else 4.3,
            "gis": 2.8 if is_general else 2.1,
            "python": 4.2 if is_general else 3.8,
            "machineLearning": 2.9 if is_general else 2.7,
        },
        "courses": [],
        "assignments": [],
        "assessmentHistory": [
            {
                "id": "PUB-ASM-01" if is_general else "ASM-001-STA-1",
                "domain": "statisticalMethods",
                "title": "Open Statistical Data & Survey Literacy" if is_general else "Statistical Methods Assessment 1",
                "score": 82 if is_general else 78,
                "maxScore": 100,
                "attempt": 1,
                "status": "Completed",
                "date": "2026-08-15",
            },
            {
                "id": "PUB-ASM-02" if is_general else "ASM-001-PYT-1",
                "domain": "python",
                "title": "Python for Microdata Analysis (Pandas/NumPy)" if is_general else "Python Assessment 1",
                "score": 89 if is_general else 75,
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
            "track": "Citizen Data Science & Open Statistics Learning Track" if is_general else "Official Statistical Cadre Capacity Track",
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
    ensure_competency_shape(record)
    return record


def resolve_login(dataset: dict[str, Any], email: str, password: str) -> tuple[dict[str, Any], dict[str, Any]] | None:
    # Primary dataset credentials
    record = find_user_record(dataset, email)
    if record:
        profile = record.get("profile") or {}
        stored_pw = str(profile.get("password", ""))
        if secrets.compare_digest(stored_pw, password) or secrets.compare_digest(stored_pw.strip(), password.strip()):
            return record, profile

    # Demo credentials from demo.json (supports both officer and general public learner)
    demo = read_demo()
    for user_key in ("user", "public_user", "officer_user"):
        demo_user = demo.get(user_key)
        if not demo_user or not isinstance(demo_user, dict):
            continue
        if email.strip().lower() == str(demo_user.get("email", "")).strip().lower():
            stored_pw = str(demo_user.get("password", ""))
            if secrets.compare_digest(stored_pw, password) or secrets.compare_digest(stored_pw.strip(), password.strip()):
                user_id = str(demo_user.get("id", ""))
                record = (
                    find_user_record(dataset, user_id)
                    or find_user_record(dataset, email)
                )
                if not record:
                    record = create_user_from_demo_profile(demo_user)
                    dataset.setdefault("users", []).append(record)
                    write_dataset(dataset)
                merged_profile = deep_merge(record.get("profile") or {}, demo_user)
                return record, merged_profile

    return None



def build_user_payload(record: dict[str, Any], effective_profile: dict[str, Any] | None = None) -> dict[str, Any]:
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

    # Dynamic iGOT recommendations based on current critical skill gaps
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

    dataset = read_dataset()
    record = find_user_record(dataset, session["id"])
    if not record:
        raise HTTPException(status_code=401, detail="Session user no longer exists.")

    return record, session["profile"]


def require_admin_key(x_admin_key: str | None) -> None:
    if not x_admin_key or not secrets.compare_digest(x_admin_key, ADMIN_KEY):
        raise HTTPException(status_code=403, detail="Invalid admin API key.")


# ==========================================
# Core Platform Routes
# ==========================================

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "platform": "StatSkill AI", "version": "3.0.0"}


@app.get("/api/meta")
def meta() -> dict[str, Any]:
    dataset = read_dataset()
    return {
        "dataset": dataset.get("dataset"),
        "version": dataset.get("version"),
        "userCount": len(dataset.get("users", [])),
        "domains": list(ENGINE_DEFINITIONS.keys()),
        "igotCourseCount": len(IGOT_COURSE_CATALOG),
    }


@app.post("/api/auth/login")
def login(request: LoginRequest) -> dict[str, Any]:
    dataset = read_dataset()
    resolved = resolve_login(dataset, str(request.email), request.password)
    if not resolved:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    record, profile = resolved
    # Ensure competency structures are computed
    ensure_competency_shape(record)

    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {"id": record["id"], "profile": profile}

    return {
        "access_token": token,
        "token_type": "bearer",
        "data": build_user_payload(record, profile),
    }


@app.post("/api/auth/register")
def register(request: RegisterRequest) -> dict[str, Any]:
    dataset = read_dataset()
    existing = find_user_record(dataset, request.email)
    if existing is not None:
        raise HTTPException(
            status_code=400,
            detail="An account with this email address already exists.",
        )

    new_id = f"USR-{len(dataset.get('users', [])) + 1:03d}"
    emp_code = f"EMP-{secrets.randbelow(90000) + 10000}"
    new_user: dict[str, Any] = {
        "id": new_id,
        "employeeCode": emp_code,
        "profile": {
            "name": request.name.strip(),
            "email": request.email.strip().lower(),
            "password": request.password,
            "role": request.role,
            "department": request.department,
            "projectId": request.projectId,
        },
        "dashboard": {
            "overallCompetency": 62,
            "overallCompetencyLabel": "62/100",
            "rank": "B",
            "level": 60,
            "xp": 1200,
            "criticalSkillGaps": 2,
            "moderateSkillGaps": 3,
            "strongSkills": 1,
            "assessmentsCompleted": 0,
            "learningProgress": 10,
            "completedModules": 0,
            "totalModules": 5,
        },
        "competencyScores": {
            "statisticalMethods": 2.8,
            "nationalAccounts": 2.2,
            "priceIndices": 2.4,
            "dataQuality": 2.7,
            "gis": 2.1,
            "python": 2.6,
            "machineLearning": 2.0,
        },
        "courses": [],
        "assignments": [],
        "assessmentHistory": [],
        "documents": [],
        "certificates": [],
        "notifications": [
            {
                "id": "NOTIF-01",
                "title": f"Welcome to StatSkill AI, {request.name.strip()}!",
                "time": "Just now",
                "color": "cyan",
            }
        ],
        "rawInputs": {
            "selfAssessment": {
                "statisticalMethods": [2.8, 2.8],
                "nationalAccounts": [2.2, 2.2],
                "priceIndices": [2.4, 2.4],
                "dataQuality": [2.7, 2.7],
                "gis": [2.1, 2.1],
                "python": [2.6, 2.6],
            },
            "learningHours": {
                "statisticalMethods": 0,
                "nationalAccounts": 0,
                "priceIndices": 0,
                "dataQuality": 0,
                "gis": 0,
                "python": 0,
            },
        },
        "learningPath": {
            "track": "Official Statistical Cadre Capacity Track",
            "modulesCompleted": 0,
            "totalModules": 5,
            "modules": [
                {"step": 1, "title": "Official Statistics Foundations", "status": "In Progress", "duration": "4h", "lessons": 6, "progress": 15, "state": "active"},
                {"step": 2, "title": "Survey Sampling & Estimation", "status": "Upcoming", "duration": "6h", "lessons": 8, "progress": 0, "state": "locked"},
                {"step": 3, "title": "National Accounts & Macro Deflators", "status": "Upcoming", "duration": "8h", "lessons": 10, "progress": 0, "state": "locked"},
                {"step": 4, "title": "Price Statistics & Index Compilation", "status": "Upcoming", "duration": "5h", "lessons": 7, "progress": 0, "state": "locked"},
                {"step": 5, "title": "Data Quality Assurance & Audits", "status": "Upcoming", "duration": "6h", "lessons": 8, "progress": 0, "state": "locked"},
            ],
        },
    }

    ensure_competency_shape(new_user)
    dataset.setdefault("users", []).append(new_user)
    write_dataset(dataset)

    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {"id": new_user["id"], "profile": new_user["profile"]}

    return {
        "access_token": token,
        "token_type": "bearer",
        "data": build_user_payload(new_user, new_user["profile"]),
    }


@app.post("/api/auth/logout")
def logout(authorization: str | None = Header(default=None)) -> dict[str, bool]:
    if authorization and authorization.lower().startswith("bearer "):
        SESSIONS.pop(authorization.split(" ", 1)[1].strip(), None)
    return {"ok": True}


@app.get("/api/me")
def me(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    record, profile = session_record(authorization)
    return {"user": build_user_payload(record, profile)["user"], "data": build_user_payload(record, profile)}


@app.get("/api/me/data")
def my_data(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    record, profile = session_record(authorization)
    return build_user_payload(record, profile)


@app.get("/api/users/{email_or_id}/data")
def public_demo_lookup(email_or_id: str) -> dict[str, Any]:
    dataset = read_dataset()
    record = find_user_record(dataset, email_or_id)

    if record is None:
        demo = read_demo()
        for user_key in ("user", "public_user", "officer_user"):
            demo_user = demo.get(user_key)
            if not demo_user or not isinstance(demo_user, dict):
                continue
            candidates = [str(demo_user.get("id", "")), str(demo_user.get("email", ""))]
            if any(email_or_id.strip().lower() == c.strip().lower() for c in candidates):
                record = find_user_record(dataset, str(demo_user.get("id", "")))
                if record:
                    return build_user_payload(record, deep_merge(record.get("profile") or {}, demo_user))

    if record is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return build_user_payload(record)


# ==========================================
# Document Ingestion & AI MCQ Generation
# ==========================================

@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """
    Accepts PDF, DOCX, PPTX, or TXT learning materials, extracts text,
    creates semantic chunks, and adds it to the officer's Document Vault.
    """
    record, profile = session_record(authorization)
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        extracted_text = extract_document_text(file.filename or "uploaded_file", content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to extract document: {exc}")

    # Store file locally in uploads folder
    safe_filename = f"{record['id']}_{secrets.token_hex(4)}_{Path(file.filename or 'file').name}"
    save_path = UPLOAD_DIR / safe_filename
    save_path.write_bytes(content)

    chunks = chunk_document(extracted_text)
    word_count = len(extracted_text.split())

    # Infer domain category from content
    lower_txt = extracted_text.lower()
    category = "General Statistics"
    if "sample" in lower_txt or "sampling" in lower_txt or "strata" in lower_txt:
        category = "Survey Methodology"
    elif "gdp" in lower_txt or "gva" in lower_txt or "national accounts" in lower_txt:
        category = "National Accounts"
    elif "cpi" in lower_txt or "price" in lower_txt or "inflation" in lower_txt:
        category = "Price Indices"
    elif "quality" in lower_txt or "validation" in lower_txt or "imputation" in lower_txt:
        category = "Data Quality"
    elif "gis" in lower_txt or "spatial" in lower_txt or "map" in lower_txt:
        category = "GIS & Spatial"

    doc_entry = {
        "id": f"DOC-{len(record.get('documents', [])) + 1:03d}",
        "name": file.filename or "Uploaded Document",
        "category": category,
        "size": f"{max(1, len(content) // 1024)} KB",
        "uploadDate": "Just now",
        "wordCount": word_count,
        "chunksCount": len(chunks),
        "summary": extracted_text[:300].strip() + ("..." if len(extracted_text) > 300 else ""),
        "extractedText": extracted_text,
        "shared": False,
        "addedThisMonth": True,
    }

    record.setdefault("documents", []).insert(0, doc_entry)

    # Persist in dataset
    dataset = read_dataset()
    for idx, candidate in enumerate(dataset.get("users", [])):
        if candidate.get("id") == record.get("id"):
            dataset["users"][idx] = record
            break
    write_dataset(dataset)

    return {
        "ok": True,
        "document": doc_entry,
        "extractedSample": extracted_text[:500],
        "chunks": chunks[:3],
    }


@app.get("/api/documents")
def get_documents(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    record, _ = session_record(authorization)
    return {"documents": record.get("documents", [])}


def create_minimal_pdf_bytes(title: str, subtitle: str, paragraphs: list[str]) -> bytes:
    def escape_pdf(text: str) -> str:
        clean = "".join(c for c in text if 32 <= ord(c) < 127)
        return clean.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    text_commands = [
        "BT",
        "/F1 16 Tf",
        "50 740 Td",
        f"({escape_pdf(title)}) Tj",
        "/F1 10 Tf",
        "0 -22 Td",
        f"({escape_pdf(subtitle)}) Tj",
        "0 -18 Td",
        "(--------------------------------------------------------------------------------) Tj",
        "/F1 9 Tf",
    ]
    for p in paragraphs[:24]:
        text_commands.append("0 -15 Td")
        text_commands.append(f"({escape_pdf(p[:95])}) Tj")
    text_commands.append("ET")
    stream_content = "\n".join(text_commands).encode("latin-1", errors="replace")

    pdf_parts = [
        b"%PDF-1.4\n",
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n",
        f"4 0 obj\n<< /Length {len(stream_content)} >>\nstream\n".encode("ascii"),
        stream_content,
        b"\nendstream\nendobj\n",
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]

    body = b"".join(pdf_parts)
    o1 = body.find(b"1 0 obj")
    o2 = body.find(b"2 0 obj")
    o3 = body.find(b"3 0 obj")
    o4 = body.find(b"4 0 obj")
    o5 = body.find(b"5 0 obj")
    xref_pos = len(body)
    xref = (
        f"xref\n0 6\n"
        f"0000000000 65535 f \n"
        f"{o1:010d} 00000 n \n"
        f"{o2:010d} 00000 n \n"
        f"{o3:010d} 00000 n \n"
        f"{o4:010d} 00000 n \n"
        f"{o5:010d} 00000 n \n"
        f"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n"
    ).encode("ascii")
    return body + xref


@app.get("/api/documents/{doc_id}/download")
def download_document(
    doc_id: str,
    authorization: str | None = Header(default=None),
) -> Response:
    """
    Downloads an authentic document from the user's Document Vault.
    Supports uploaded files and standard MoSPI learning materials.
    """
    dataset = read_dataset()
    user_record: dict[str, Any] | None = None
    if authorization:
        try:
            user_record, _ = session_record(authorization)
        except Exception:
            user_record = None

    target_doc: dict[str, Any] | None = None
    if user_record:
        for doc in user_record.get("documents", []):
            if doc.get("id") == doc_id:
                target_doc = doc
                break

    if not target_doc:
        for user in dataset.get("users", []):
            for doc in user.get("documents", []):
                if doc.get("id") == doc_id:
                    target_doc = doc
                    break
            if target_doc:
                break

    if not target_doc:
        demo = read_demo()
        for doc in demo.get("documents", []):
            if doc.get("id") == doc_id:
                target_doc = doc
                break

    if not target_doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    doc_name = str(target_doc.get("name", f"{doc_id}.pdf"))

    # Check if a matching uploaded file exists on disk
    if user_record:
        safe_prefix = f"{user_record['id']}_"
        for file_path in UPLOAD_DIR.glob(f"{safe_prefix}*"):
            if file_path.name.endswith(Path(doc_name).name):
                return FileResponse(file_path, filename=doc_name)

    # For standard study materials, generate authentic MoSPI PDF
    title = f"StatSkill AI — {Path(doc_name).stem}"
    subtitle = f"Ministry of Statistics & Programme Implementation (MoSPI) · {target_doc.get('category', 'Learning Resource')}"
    summary = str(target_doc.get("summary") or target_doc.get("extractedText") or "")
    if not summary:
        summary = (
            "National Statistical System Capacity Building & Assessment Framework. "
            "Coordinated by the National Statistical Systems Training Academy (NSSTA) and MoSPI. "
            "Curriculum aligned to FRAC (Framework for Roles, Activities and Competencies)."
        )

    paragraphs = [
        f"Document ID: {doc_id}",
        f"Category: {target_doc.get('category', 'General Statistics')}",
        "Verification: MoSPI Central Directory Certified Resource",
        "--------------------------------------------------------------------------------",
        "Course Study Guide & Methodological Syllabus:",
        summary[:200],
        summary[200:400] if len(summary) > 200 else "Standard operating procedure for data collection, validation, and estimation.",
        summary[400:600] if len(summary) > 400 else "Official statistical indicators and computational formulas.",
        "--------------------------------------------------------------------------------",
        "Learning Objectives & Competency Benchmarks:",
        "1. Understand fundamental survey concepts, rotating panels, and strata weighting.",
        "2. Detect outliers, impute missing values, and validate enterprise microdata.",
        "3. Apply computational algorithms in Python/Pandas for statistical indicators.",
        "4. Comply with Government of India NDSAP guidelines and data security norms.",
        "National Statistical Office · Government of India · 2026",
    ]

    pdf_bytes = create_minimal_pdf_bytes(title, subtitle, paragraphs)
    safe_doc_name = doc_name.replace("–", "-").replace("—", "-")
    safe_doc_name = "".join(c for c in safe_doc_name if 32 <= ord(c) < 128)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{safe_doc_name}"'},
    )



@app.post("/api/mcq/generate")
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

    return {
        "ok": True,
        "questionCount": len(questions),
        "difficulty": request.difficulty,
        "bloomLevel": request.bloom_level,
        "domain": request.domain or "General Statistics",
        "questions": questions,
    }


# ==========================================
# Assessment Execution & Reassessment Loop
# ==========================================

@app.get("/api/assessments/available")
def get_available_assessments(authorization: str | None = Header(default=None)) -> dict[str, Any]:
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


@app.post("/api/assessments/submit")
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

    total = len(request.answers)
    correct = sum(1 for a in request.answers if a.is_correct)
    percentage = round((correct / total) * 100, 1)

    answers_detail = [a.model_dump() for a in request.answers]
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


# ==========================================
# iGOT Karmayogi Connector & FRAC Services
# ==========================================

@app.get("/api/igot/courses")
def igot_courses(
    domain: str | None = None,
    level: str | None = None,
) -> dict[str, Any]:
    """Returns the official iGOT Karmayogi course catalog for India's Official Statistical System."""
    courses = get_all_courses(domain=domain, level=level)
    return {"courses": courses, "total": len(courses)}


@app.get("/api/igot/recommendations")
def igot_recommendations(authorization: str | None = Header(default=None)) -> dict[str, Any]:
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


@app.post("/api/igot/enroll")
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
    # Check if already enrolled
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


@app.get("/api/competencies/framework")
def competency_framework() -> dict[str, Any]:
    """Returns the official MoSPI FRAC competency framework definitions and benchmarks."""
    return {
        "framework": "Mission Karmayogi FRAC - MoSPI Official Statistical Cadre",
        "definitions": ENGINE_DEFINITIONS,
    }


# ==========================================
# Admin & User Profile Endpoints
# ==========================================

@app.get("/api/admin/users")
def admin_users(x_admin_key: str | None = Header(default=None)) -> dict[str, Any]:
    require_admin_key(x_admin_key)
    dataset = read_dataset()
    return {
        "users": [
            {
                "id": record.get("id"),
                "employeeCode": record.get("employeeCode"),
                "name": (record.get("profile") or {}).get("name"),
                "email": (record.get("profile") or {}).get("email"),
                "role": (record.get("profile") or {}).get("role"),
            }
            for record in dataset.get("users", [])
        ]
    }


@app.put("/api/admin/users/{user_id}")
def admin_patch_user(
    user_id: str,
    request: AdminUserPatch,
    x_admin_key: str | None = Header(default=None),
) -> dict[str, Any]:
    require_admin_key(x_admin_key)
    dataset = read_dataset()
    record = find_user_record(dataset, user_id)
    if record is None:
        raise HTTPException(status_code=404, detail="User not found.")

    patch = request.data
    if isinstance(patch.get("competencyScores"), dict):
        existing = record.setdefault("competencyScores", {})
        existing.update(patch["competencyScores"])

    if isinstance(patch.get("competencies"), list):
        record["competencies"] = copy.deepcopy(patch["competencies"])

    for key, value in patch.items():
        if key not in {"competencyScores", "competencies"}:
            if isinstance(value, dict) and isinstance(record.get(key), dict):
                record[key] = deep_merge(record[key], value)
            else:
                record[key] = copy.deepcopy(value)

    ensure_competency_shape(record)
    for idx, candidate in enumerate(dataset.get("users", [])):
        if candidate.get("id") == record.get("id"):
            dataset["users"][idx] = record
            break

    write_dataset(dataset)
    return build_user_payload(record)


@app.put("/api/admin/dataset")
def admin_replace_dataset(
    request: AdminDatasetUpdate,
    x_admin_key: str | None = Header(default=None),
) -> dict[str, Any]:
    require_admin_key(x_admin_key)
    data = request.data
    if not isinstance(data.get("users"), list):
        raise HTTPException(status_code=400, detail="data.users must be an array.")
    for record in data["users"]:
        if not isinstance(record, dict) or not record.get("id") or not isinstance(record.get("profile"), dict):
            raise HTTPException(status_code=400, detail="Every user needs id and profile.")

    write_dataset(data)
    return {"ok": True, "userCount": len(data["users"])}


@app.put("/api/me/profile")
def update_profile(
    request: UserUpdateRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    record, profile = session_record(authorization)
    if request.name is not None:
        cleaned = request.name.strip()
        if not cleaned:
            raise HTTPException(status_code=400, detail="Name cannot be empty.")
        record.setdefault("profile", {})["name"] = cleaned
        profile["name"] = cleaned

    dataset = read_dataset()
    for idx, candidate in enumerate(dataset.get("users", [])):
        if candidate.get("id") == record.get("id"):
            dataset["users"][idx] = record
            break
    write_dataset(dataset)
    return build_user_payload(record, profile)


@app.get("/api/data-sources")
def get_official_data_sources() -> dict[str, Any]:
    """
    Returns the comprehensive catalog of official National Statistical System data sources.
    """
    if DATA_SOURCES_FILE.exists():
        try:
            return json.loads(DATA_SOURCES_FILE.read_text(encoding="utf-8"))
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Failed to read data sources: {exc}") from exc
    return {"title": "Official Statistical Data Sources", "data_sources": []}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
