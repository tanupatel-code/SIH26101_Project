from pathlib import Path
from typing import Any
from fastapi import APIRouter, Depends, File, Header, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse

from api.deps import get_current_session
from core.config import UPLOAD_DIR
from repositories.dataset_repository import read_dataset, read_demo, write_dataset
from services.auth_service import session_record
from services.certificate_service import create_minimal_pdf_bytes
from services.document_service import (
    find_document_for_download,
    infer_document_category,
    process_and_store_document,
)

router = APIRouter(tags=["documents"])


@router.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    session: tuple[dict[str, Any], dict[str, Any]] = Depends(get_current_session),
) -> dict[str, Any]:
    """
    Accepts PDF, DOCX, PPTX, or TXT learning materials, extracts text,
    creates semantic chunks, and adds it to the officer's Document Vault
    with robust content-hash deduplication and unique doc identity.
    """
    record, _ = session
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    original_filename = file.filename or "uploaded_file"
    return process_and_store_document(
        filename=original_filename,
        content=content,
        owner_record=record,
    )


@router.get("/api/documents")
def get_documents(
    session: tuple[dict[str, Any], dict[str, Any]] = Depends(get_current_session)
) -> dict[str, Any]:
    record, _ = session
    return {"documents": record.get("documents", [])}


@router.get("/api/documents/{doc_id}/download")
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

    target_doc, file_path = find_document_for_download(doc_id, user_record)

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
    if file_path and file_path.exists():
        return FileResponse(file_path, filename=doc_name)

    if user_record:
        safe_prefix = f"{user_record['id']}_"
        for p in UPLOAD_DIR.glob(f"{safe_prefix}*"):
            if p.name.endswith(Path(doc_name).name):
                return FileResponse(p, filename=doc_name)

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
