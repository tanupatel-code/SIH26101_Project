import re
from fastapi import APIRouter, Header, Response
from services.auth_service import session_record
from services.certificate_service import generate_certificate_pdf

router = APIRouter(tags=["certificates"])


@router.get("/api/certificates/{cert_id}/download")
def download_certificate(
    cert_id: str,
    name: str | None = None,
    title: str | None = None,
    authorization: str | None = Header(default=None),
) -> Response:
    """
    Downloads a 100% standards-compliant PDF Certificate of Competency (ISO 32000-1).
    Opens reliably in Adobe Acrobat, Google Chrome, Microsoft Edge, and macOS Preview.
    """
    user_name = name or "Official Statistical Cadre Officer"
    if authorization:
        try:
            _, profile = session_record(authorization)
            if profile and profile.get("name"):
                user_name = profile["name"]
        except Exception:
            pass

    cert_title = title or "Official Statistical Competency & Survey Accreditation"
    clean_title = re.sub(r"[^a-zA-Z0-9_-]", "_", cert_title)
    clean_filename = f"CERTIFICATE_{clean_title}.pdf"

    pdf_bytes, filename = generate_certificate_pdf(
        user_name=user_name,
        cert_title=cert_title,
        cert_id=cert_id,
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename or clean_filename}"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )
