"""
Document parsing and text extraction service for StatSkill AI.
Supports PDF, DOCX, TXT, Markdown, and PPTX learning materials.
"""

from __future__ import annotations

import io
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

pypdf: Any = None
try:
    import pypdf as _pypdf
    pypdf = _pypdf
except ImportError:
    pypdf = None

docx: Any = None
try:
    import docx as _docx
    docx = _docx
except ImportError:
    docx = None


def extract_text_from_txt(content: bytes) -> str:
    """Extract text from plain text or markdown content."""
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return content.decode(enc)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF using pypdf."""
    if pypdf is None:
        return "PDF extractor library (pypdf) is not available."
    try:
        reader = pypdf.PdfReader(io.BytesIO(content))
        pages_text = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages_text.append(text.strip())
        return "\n\n".join(pages_text)
    except Exception as exc:
        raise ValueError(f"Failed to parse PDF document: {exc}") from exc


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    if docx is None:
        return "DOCX extractor library (python-docx) is not available."
    try:
        doc = docx.Document(io.BytesIO(content))
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)
        return "\n\n".join(paragraphs)
    except Exception as exc:
        raise ValueError(f"Failed to parse DOCX document: {exc}") from exc


def extract_text_from_pptx(content: bytes) -> str:
    """Extract text from PPTX by parsing slide XMLs directly."""
    try:
        with zipfile.ZipFile(io.BytesIO(content), "r") as z:
            slide_names = sorted(
                [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")],
                key=lambda x: int("".join(filter(str.isdigit, x)) or 0)
            )
            slides_text = []
            for sname in slide_names:
                xml_data = z.read(sname)
                root = ET.fromstring(xml_data)
                texts = [node.text.strip() for node in root.iter() if node.text and node.text.strip()]
                if texts:
                    slides_text.append(" ".join(texts))
            return "\n\n".join(slides_text)
    except Exception as exc:
        raise ValueError(f"Failed to parse PPTX document: {exc}") from exc


def extract_document_text(filename: str, content: bytes) -> str:
    """Unified document text extractor based on file extension."""
    suffix = Path(filename).suffix.lower()
    if suffix in (".pdf",):
        text = extract_text_from_pdf(content)
    elif suffix in (".docx", ".doc"):
        text = extract_text_from_docx(content)
    elif suffix in (".pptx", ".ppt"):
        text = extract_text_from_pptx(content)
    elif suffix in (".txt", ".md", ".csv", ".json"):
        text = extract_text_from_txt(content)
    else:
        text = extract_text_from_txt(content)

    cleaned = re.sub(r"[ \t]+", " ", text)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def chunk_document(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[dict[str, Any]]:
    """Splits document text into manageable semantic chunks for RAG or MCQ generation."""
    if not text.strip():
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[dict[str, Any]] = []
    current_chunk: list[str] = []
    current_length = 0

    for p in paragraphs:
        p_len = len(p)
        if current_length + p_len > chunk_size and current_chunk:
            combined = "\n\n".join(current_chunk)
            chunks.append({
                "chunk_id": len(chunks) + 1,
                "text": combined,
                "length": len(combined),
            })
            # keep overlap if possible
            current_chunk = [current_chunk[-1]] if len(current_chunk) > 1 else []
            current_length = sum(len(c) for c in current_chunk)

        current_chunk.append(p)
        current_length += p_len

    if current_chunk:
        combined = "\n\n".join(current_chunk)
        chunks.append({
            "chunk_id": len(chunks) + 1,
            "text": combined,
            "length": len(combined),
        })

    return chunks
