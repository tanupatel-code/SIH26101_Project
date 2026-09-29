from __future__ import annotations

import hashlib
import re
import secrets
import time
from pathlib import Path
from typing import Any
from fastapi import HTTPException

from core.config import UPLOAD_DIR
from repositories.dataset_repository import read_dataset, write_dataset
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


def process_and_store_document(
    filename: str,
    content: bytes,
    owner_record: dict[str, Any],
) -> dict[str, Any]:
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    original_filename = Path(filename or "uploaded_file").name
    # Clean non-printable characters
    original_filename = re.sub(r"[^\w\s\.-]", "_", original_filename)

    try:
        extracted_text = extract_document_text(original_filename, content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to extract document: {exc}")

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
    safe_filename = f"{owner_id}_{content_hash[:8]}_{original_filename}"
    save_path = UPLOAD_DIR / safe_filename
    save_path.write_bytes(content)

    chunks = chunk_document(extracted_text)
    word_count = len(extracted_text.split())
    category = infer_document_category(extracted_text)

    doc_entry = {
        "id": doc_id,
        "name": original_filename,
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
    owner_record: dict[str, Any] | None,
) -> tuple[dict[str, Any] | None, Path | None]:
    target_doc = None
    if owner_record:
        for d in owner_record.get("documents", []):
            if d.get("id") == doc_id:
                target_doc = d
                break

    if not target_doc:
        dataset = read_dataset()
        for u in dataset.get("users", []):
            for d in u.get("documents", []):
                if d.get("id") == doc_id:
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
