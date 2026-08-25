"""Validación y almacenamiento de documentos de voluntarios."""
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from config import MAX_UPLOAD_SIZE_MB, UPLOAD_DIR

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}
EXTENSION_BY_MIME = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}


class InvalidVolunteerDocument(ValueError):
    """Permite traducir errores de archivo a respuestas HTTP 400."""


def _upload_root() -> Path:
    root = Path(__file__).resolve().parents[2] / UPLOAD_DIR
    root.mkdir(parents=True, exist_ok=True)
    return root


def _detect_mime_type(content: bytes) -> str | None:
    if content.startswith(b"%PDF-"):
        return "application/pdf"
    if content.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    return None


def validate_and_store_documents(
    volunteer_id: int,
    files: list[UploadFile],
) -> list[dict[str, str]]:
    """Valida y guarda los documentos adjuntos de un voluntario."""

    if not files:
        return []

    stored_documents: list[dict[str, str]] = []
    volunteer_dir = _upload_root() / str(volunteer_id)
    volunteer_dir.mkdir(parents=True, exist_ok=True)
    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024

    for upload in files:
        if upload.filename is None or upload.filename.strip() == "":
            raise InvalidVolunteerDocument("Cada archivo debe tener un nombre válido.")

        original_name = Path(upload.filename).name
        extension = Path(original_name).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise InvalidVolunteerDocument(
                f"Formato no permitido: {extension}. Usa pdf, jpg o png."
            )

        content = upload.file.read()
        if not content:
            raise InvalidVolunteerDocument(
                f"El archivo '{original_name}' está vacío."
            )
        if len(content) > max_bytes:
            raise InvalidVolunteerDocument(
                f"El archivo '{original_name}' supera el límite de "
                f"{MAX_UPLOAD_SIZE_MB} MB."
            )

        mime_type = upload.content_type or _detect_mime_type(content)
        if mime_type not in ALLOWED_MIME_TYPES:
            raise InvalidVolunteerDocument(
                f"Tipo de archivo no permitido para '{original_name}'."
            )

        safe_extension = EXTENSION_BY_MIME.get(mime_type, extension)
        stored_name = f"{uuid4().hex}{safe_extension}"
        stored_path = volunteer_dir / stored_name
        stored_path.write_bytes(content)

        stored_documents.append(
            {
                "nombre_original": original_name,
                "ruta": str(stored_path.relative_to(_upload_root().parent)),
                "tipo_mime": mime_type,
            }
        )

    return stored_documents
