"""Orquestación de negocio del módulo de voluntariado."""
import secrets
import logging
from typing import Any

from fastapi import UploadFile

from config import BASE_URL
from modules.voluntariado import email_service, models
from modules.voluntariado.file_service import validate_and_store_documents
from modules.voluntariado.schemas import VolunteerCreate, VolunteerFrontendCreate, VolunteerStatus
logger = logging.getLogger(__name__)

def _build_document_response(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": document["id"],
        "nombre_original": document["nombre_original"],
        "tipo_mime": document["tipo_mime"],
        "creado_en": document["creado_en"],
    }


def _build_registration_response(volunteer: dict[str, Any]) -> dict[str, Any]:
    documents = models.get_volunteer_documents(volunteer["id"])
    public_volunteer = dict(volunteer)
    public_volunteer.pop("admin_token", None)
    public_volunteer.pop("volunteer_token", None)
    return {
        **public_volunteer,
        "documentos": [_build_document_response(document) for document in documents],
    }


def _build_pending_response(volunteer: dict[str, Any]) -> dict[str, Any]:
    documents = models.get_volunteer_documents(volunteer["id"])
    return {
        **volunteer,
        "documentos": [_build_document_response(document) for document in documents],
    }


def register_volunteer(
    volunteer_data: VolunteerCreate,
    documents: list[UploadFile],
) -> dict[str, Any]:
    """Registra una solicitud pendiente, guarda documentos y avisa al admin."""

    admin_token = secrets.token_urlsafe(32)
    volunteer_token = secrets.token_urlsafe(32)

    volunteer = models.create_volunteer_pending(
        name=volunteer_data.name,
        contact=volunteer_data.contact,
        skills=volunteer_data.skills,
        availability=volunteer_data.availability,
        admin_token=admin_token,
        volunteer_token=volunteer_token,
    )

    stored_documents: list[dict[str, Any]] = []
    file_metadata = validate_and_store_documents(volunteer["id"], documents)
    for metadata in file_metadata:
        stored_documents.append(
            models.save_volunteer_document(
                volunteer_id=volunteer["id"],
                original_name=metadata["nombre_original"],
                stored_path=metadata["ruta"],
                mime_type=metadata["tipo_mime"],
            )
        )

    approve_url = (
        f"{BASE_URL}/api/voluntarios/{volunteer['id']}/aprobar?token={admin_token}"
    )
    reject_url = (
        f"{BASE_URL}/api/voluntarios/{volunteer['id']}/rechazar?token={admin_token}"
    )
    
    try:
        email_service.send_admin_new_volunteer_email(
            volunteer=volunteer,
            documents=stored_documents,
            approve_url=approve_url,
            reject_url=reject_url,
        )
    except Exception:
        logger.exception(
            "No se pudo enviar el correo administrativo del voluntario %s. "
            "La solicitud permanece registrada.",
            volunteer["id"],
        )

    return _build_registration_response(volunteer)


def register_volunteer_from_frontend(
    volunteer_data: VolunteerFrontendCreate,
) -> dict[str, Any]:
    """Registra una solicitud pendiente desde el formulario frontend."""

    admin_token = secrets.token_urlsafe(32)
    volunteer_token = secrets.token_urlsafe(32)

    volunteer = models.create_volunteer_pending_from_frontend(
        data=volunteer_data,
        admin_token=admin_token,
        volunteer_token=volunteer_token,
    )

    approve_url = (
        f"{BASE_URL}/api/voluntarios/{volunteer['id']}/aprobar?token={admin_token}"
    )
    reject_url = (
        f"{BASE_URL}/api/voluntarios/{volunteer['id']}/rechazar?token={admin_token}"
    )
    try:
        email_service.send_admin_new_volunteer_email(
            volunteer=models.get_volunteer(volunteer["id"]),
            documents=[],
            approve_url=approve_url,
            reject_url=reject_url,
        )
    except Exception:
        logger.exception(
            "No se pudo enviar el correo administrativo del voluntario %s. "
            "La solicitud permanece registrada.",
            volunteer["id"],
        )

    return volunteer


def approve_volunteer(
    volunteer_id: int,
    *,
    admin_token: str | None = None,
    via_api: bool = False,
) -> dict[str, Any]:
    """Aprueba una solicitud pendiente y notifica al voluntario."""

    if via_api:
        volunteer = models.get_volunteer(volunteer_id)
    else:
        if admin_token is None:
            raise ValueError("Missing admin token")
        volunteer = models.get_volunteer_by_admin_token(volunteer_id, admin_token)

    if volunteer is None:
        return {"error": "not_found"}

    if volunteer["estado"] != VolunteerStatus.PENDING.value:
        return {"error": "invalid_transition"}

    approved = models.approve_volunteer_record(volunteer_id)
    if approved is None:
        return {"error": "not_found"}

    availability_url = (
        f"{BASE_URL}/api/voluntarios/{volunteer_id}/disponible"
        f"?token={approved['volunteer_token']}"
    )
    email_service.send_volunteer_approved_email(
        volunteer=approved,
        availability_url=availability_url,
    )

    return {
        "id": approved["id"],
        "estado": approved["estado"],
        "mensaje": "Voluntario aprobado correctamente.",
    }


def reject_volunteer(
    volunteer_id: int,
    *,
    admin_token: str | None = None,
    via_api: bool = False,
) -> dict[str, Any]:
    """Rechaza una solicitud pendiente y notifica al voluntario."""

    if via_api:
        volunteer = models.get_volunteer(volunteer_id)
    else:
        if admin_token is None:
            raise ValueError("Missing admin token")
        volunteer = models.get_volunteer_by_admin_token(volunteer_id, admin_token)

    if volunteer is None:
        return {"error": "not_found"}

    if volunteer["estado"] != VolunteerStatus.PENDING.value:
        return {"error": "invalid_transition"}

    rejected = models.reject_volunteer_record(volunteer_id)
    if rejected is None:
        return {"error": "not_found"}

    email_service.send_volunteer_rejected_email(rejected)

    return {
        "id": rejected["id"],
        "estado": rejected["estado"],
        "mensaje": "Solicitud de voluntariado rechazada.",
    }


def update_availability(
    volunteer_id: int,
    is_available: bool,
    volunteer_token: str,
) -> dict[str, Any] | None:
    """Actualiza la disponibilidad activa de un voluntario aprobado."""

    volunteer = models.get_volunteer_by_volunteer_token(
        volunteer_id,
        volunteer_token,
    )

    if volunteer is None:
        return None

    return models.update_volunteer_availability(
        volunteer_id=volunteer_id,
        is_available=is_available,
    )
