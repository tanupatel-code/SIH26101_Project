"""
StatSkill AI — Production Backend Application Bootstrap & Composition Layer
Ministry of Statistics & Programme Implementation (MoSPI)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure backend root is on sys.path for direct imports
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Core configuration & file locations
from core.config import (
    ADMIN_KEY,
    CORS_ORIGINS,
    DATA_FILE,
    DATA_SOURCES_FILE,
    DEMO_FILE,
    UPLOAD_DIR,
)

# Schema contracts
from schemas.admin_schemas import (
    AdminDatasetUpdate,
    AdminUserPatch,
    EnrollRequest,
)
from schemas.assessment_schemas import (
    McqGenerateRequest,
    QuizAnswerItem,
    QuizSubmitRequest,
)
from schemas.auth_schemas import (
    LoginRequest,
    RegisterRequest,
    UserUpdateRequest,
)

# Repositories
from repositories.dataset_repository import (
    read_data_sources,
    read_dataset,
    read_demo,
    write_dataset,
)

# Services
from services.assessment_service import record_quiz_submission
from services.auth_service import (
    SESSIONS,
    build_user_payload,
    create_user_from_demo_profile,
    deep_merge,
    find_user_record,
    resolve_login,
    sanitize_profile,
    session_record,
)
from services.certificate_service import (
    create_minimal_pdf_bytes,
    generate_certificate_pdf,
)
from services.competency_service import (
    ENGINE_DEFINITIONS,
    avg,
    calculate_competency_scores,
    ensure_competency_shape,
    is_number,
)
from services.document_parser import (
    chunk_document,
    extract_document_text,
    extract_text_from_txt,
)
from services.igot_service import (
    IGOT_COURSE_CATALOG,
    get_all_courses,
    recommend_courses_for_gaps,
)
from services.mcq_generator import (
    OFFICIAL_STATS_CONCEPTS,
    extract_keywords_from_text,
    generate_mcqs_from_text,
)

# API Routers
from api.admin import router as admin_router
from api.assessments import router as assessments_router
from api.auth import router as auth_router
from api.certificates import download_certificate
from api.certificates import router as certificates_router
from api.competencies import router as competencies_router
from api.data_sources import router as data_sources_router
from api.documents import router as documents_router
from api.igot import router as igot_router
from api.system import router as system_router

# Initialize FastAPI application
app = FastAPI(
    title="StatSkill AI — MoSPI Competency Platform API",
    description="High-performance REST API for National Statistical System Competency Assessment",
    version="3.0.0",
)

# CORS configuration — strictly whitelisted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Domain Routers
app.include_router(system_router)
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(certificates_router)
app.include_router(assessments_router)
app.include_router(igot_router)
app.include_router(competencies_router)
app.include_router(data_sources_router)
app.include_router(admin_router)

__all__ = [
    "app",
    "ADMIN_KEY",
    "DATA_FILE",
    "DEMO_FILE",
    "DATA_SOURCES_FILE",
    "UPLOAD_DIR",
    "SESSIONS",
    "LoginRequest",
    "RegisterRequest",
    "McqGenerateRequest",
    "QuizSubmitRequest",
    "QuizAnswerItem",
    "AdminUserPatch",
    "AdminDatasetUpdate",
    "EnrollRequest",
    "UserUpdateRequest",
    "read_dataset",
    "write_dataset",
    "read_demo",
    "read_data_sources",
    "sanitize_profile",
    "resolve_login",
    "build_user_payload",
    "session_record",
    "create_user_from_demo_profile",
    "deep_merge",
    "find_user_record",
    "create_minimal_pdf_bytes",
    "generate_certificate_pdf",
    "download_certificate",
    "record_quiz_submission",
    "ENGINE_DEFINITIONS",
    "calculate_competency_scores",
    "ensure_competency_shape",
    "is_number",
    "avg",
    "chunk_document",
    "extract_document_text",
    "extract_text_from_txt",
    "IGOT_COURSE_CATALOG",
    "get_all_courses",
    "recommend_courses_for_gaps",
    "generate_mcqs_from_text",
    "extract_keywords_from_text",
    "OFFICIAL_STATS_CONCEPTS",
]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
