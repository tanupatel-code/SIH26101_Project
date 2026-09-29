"""
StatSkill AI — Document Processing & Ingestion Service.
Handles document extraction, chunking, categorization, content-hash deduplication,
and secure file storage with path traversal protection and authorization guards.
"""

from __future__ import annotations

import hashlib
import re
import secrets
import time
from pathlib import Path
from typing import Any
from fastapi import HTTPException

from core.config import (
    ALLOWED_UPLOAD_EXTENSIONS,
    MAX_UPLOAD_SIZE_BYTES,
    UPLOAD_DIR,
)
from repositories.dataset_repository import read_dataset, read_demo, write_dataset
from services.document_parser import extract_document_text, chunk_document


def infer_document_category(text: str) -> str:
    lower_txt = text.lower()
    if "sample" in lower_txt or "sampling" in lower_txt or "strata" in lower_txt:
        return "Survey Methodology"
    elif "gdp" in lower_txt or "gva" in lower_txt or "national accounts" in lower_txt:
        return "National Accounts"
    elif "cpi" in lower_txt or "price" in lower_txt or "inflation" in lower_txt:
        return "Price Indices"
    elif "quality" in lower_txt or "validation" in lower_txt or "imputation" in lower_txt:
        return "Data Quality"
    elif "gis" in lower_txt or "spatial" in lower_txt or "map" in lower_txt:
        return "GIS & Spatial"
    return "General Statistics"


def sanitize_filename(raw_filename: str) -> str:
    """
    Sanitizes a user-supplied filename against path traversal, control chars,
    and illegal filesystem characters.
    """
    if not raw_filename:
        return "uploaded_document.txt"

    # Remove path separators and null bytes
    cleaned = raw_filename.replace("\x00", "").replace("/", "_").replace("\\", "_")
    # Remove directory traversal patterns
    cleaned = re.sub(r"\.\.+", ".", cleaned)
    # Extract only the base filename
    base_name = Path(cleaned).name
    # Keep only safe alphanumeric, space, dot, underscore, dash
    safe_name = re.sub(r"[^\w\s\.-]", "_", base_name).strip()
    return safe_name[:200] if safe_name else "uploaded_document.txt"


def validate_upload_constraints(filename: str, file_size: int) -> None:
    """
    Validates file size and file extension against configured security policies.
    """
    if file_size > MAX_UPLOAD_SIZE_BYTES:
        max_mb = MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the maximum allowed limit of {max_mb} MB.",
        )

    clean_name = sanitize_filename(filename)
    ext = Path(clean_name).suffix.lower()
    if ext not in ALLOWED_UPLOAD_EXTENSIONS:
        allowed_list = ", ".join(sorted(ALLOWED_UPLOAD_EXTENSIONS))
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {allowed_list}",
        )


def process_and_store_document(
    filename: str,
    content: bytes,
    owner_record: dict[str, Any],
) -> dict[str, Any]:
    """
    Validates, extracts, deduplicates, and stores an uploaded document.
    Enforces file size, extension, and path traversal security.
    """
    if not content or len(content.strip()) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    validate_upload_constraints(filename, len(content))
    clean_name = sanitize_filename(filename)

    try:
        extracted_text = extract_document_text(clean_name, content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to extract document text: {exc}")

    content_hash = hashlib.sha256(content).hexdigest()
    owner_id = str(owner_record.get("id", "USR-001"))
    existing_docs = owner_record.setdefault("documents", [])

    # Check if exact same content hash already uploaded by this owner
    existing_match = None
    for doc in existing_docs:
        if doc.get("contentHash") == content_hash:
            existing_match = doc
            break

    doc_id = existing_match["id"] if existing_match else f"DOC-{secrets.token_hex(4).upper()}"
    safe_storage_name = f"{owner_id}_{content_hash[:10]}_{clean_name}"
    save_path = UPLOAD_DIR / safe_storage_name
    save_path.write_bytes(content)

    chunks = chunk_document(extracted_text)
    word_count = len(extracted_text.split())
    category = infer_document_category(extracted_text)

    doc_entry = {
        "id": doc_id,
        "name": clean_name,
        "category": category,
        "size": f"{max(1, len(content) // 1024)} KB",
        "uploadDate": time.strftime("%d %b %Y"),
        "uploadedTimestamp": int(time.time()),
        "contentHash": content_hash,
        "ownerId": owner_id,
        "wordCount": word_count,
        "chunksCount": len(chunks),
        "summary": extracted_text[:300].strip() + ("..." if len(extracted_text) > 300 else ""),
        "extractedText": extracted_text,
        "storedPath": str(save_path.name),
        "shared": False,
        "addedThisMonth": True,
        "version": (existing_match.get("version", 1) + 1) if existing_match else 1,
    }

    if existing_match:
        for idx, doc in enumerate(existing_docs):
            if doc.get("id") == existing_match["id"]:
                existing_docs[idx] = doc_entry
                break
    else:
        existing_docs.insert(0, doc_entry)

    # Persist in dataset
    dataset = read_dataset()
    for idx, candidate in enumerate(dataset.get("users", [])):
        if candidate.get("id") == owner_record.get("id"):
            dataset["users"][idx] = owner_record
            break
    write_dataset(dataset)

    return {
        "ok": True,
        "document": doc_entry,
        "extractedSample": extracted_text[:500],
        "chunks": chunks[:3],
    }


def find_document_for_download(
    doc_id: str,
    user_record: dict[str, Any] | None,
) -> tuple[dict[str, Any] | None, Path | None]:
    """
    Retrieves document metadata and stored file path with strict authorization.
    Prevents cross-user unauthorized downloads.
    """
    target_doc = None

    # 1. Check in authenticated user's private vault
    if user_record:
        for d in user_record.get("documents", []):
            if d.get("id") == doc_id:
                target_doc = d
                break

    # 2. Check public/demo learning resources
    if not target_doc:
        demo = read_demo()
        for d in demo.get("documents", []):
            if d.get("id") == doc_id:
                target_doc = d
                break

    # 3. If still not found, check other users' documents for ownership/sharing status
    if not target_doc:
        dataset = read_dataset()
        for u in dataset.get("users", []):
            if user_record and u.get("id") == user_record.get("id"):
                continue
            for d in u.get("documents", []):
                if d.get("id") == doc_id:
                    # Document belongs to someone else
                    if not d.get("shared", False):
                        if user_record:
                            raise HTTPException(
                                status_code=403,
                                detail="Forbidden: You are not authorized to download this user's private document.",
                            )
                        else:
                            raise HTTPException(
                                status_code=401,
                                detail="Authentication required to access this document.",
                            )
                    target_doc = d
                    break
            if target_doc:
                break

    if not target_doc:
        return None, None

    # Check for stored binary file on disk
    stored_name = target_doc.get("storedPath")
    if stored_name:
        candidate_path = UPLOAD_DIR / stored_name
        if candidate_path.exists():
            return target_doc, candidate_path

    # Fallback search by prefix or pattern
    for p in UPLOAD_DIR.iterdir():
        if p.is_file() and target_doc.get("name") in p.name:
            return target_doc, p

    return target_doc, None
