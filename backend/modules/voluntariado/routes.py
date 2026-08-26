"""Endpoints de voluntariado (Equipo 3, núcleo).

Este archivo recibe las peticiones HTTP relacionadas con voluntarios.
La lógica de negocio vive en services.py y el acceso a datos en models.py.
"""
import json

from fastapi import (
    APIRouter,
    Depends,
    Header,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from middleware.auth import requiere_clave_organizador
from modules.voluntariado.file_service import InvalidVolunteerDocument
from modules.voluntariado.models import (
    InvalidVolunteerTransition,
    get_volunteer_documents,
    list_pending_volunteers,
    list_volunteers_for_frontend,
    update_coordination_status,
)
from modules.voluntariado.schemas import (
    VolunteerActionResponse,
    VolunteerAvailabilityUpdate,
    VolunteerCoordinationUpdate,
    VolunteerCreate,
    VolunteerFrontendCreate,
    VolunteerFrontendRegistrationResponse,
    VolunteerFrontendResponse,
    VolunteerPendingResponse,
    VolunteerResponse,
)
from modules.voluntariado import services

router = APIRouter(prefix="/api/voluntarios", tags=["voluntariado"])


def _error_response(status_code: int, error: str, detalle: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": error, "detalle": detalle},
    )


def _normalize_uploads(documentos: list[UploadFile] | None) -> list[UploadFile]:
    if not documentos:
        return []
    return [upload for upload in documentos if upload.filename]


@router.get("", response_model=list[VolunteerFrontendResponse])
def get_volunteers(
    coordination_status: str | None = Query(default=None, alias="status"),
    skill: str | None = Query(default=None, alias="habilidad"),
    is_available: bool | None = Query(default=None, alias="disponible"),
):
    """Devuelve voluntarios aprobados visibles en la app."""

    return list_volunteers_for_frontend(
        coordination_status=coordination_status,
        skill=skill,
        is_available=is_available,
    )


@router.get(
    "/pendientes",
    response_model=list[VolunteerPendingResponse],
    dependencies=[Depends(requiere_clave_organizador)],
)
def get_pending_volunteers():
    """Lista solicitudes pendientes de validación (solo administrador)."""

    pending = list_pending_volunteers()
    return [
        {
            **volunteer,
            "documentos": [
                {
                    "id": document["id"],
                    "nombre_original": document["nombre_original"],
                    "tipo_mime": document["tipo_mime"],
                    "creado_en": document["creado_en"],
                }
                for document in get_volunteer_documents(volunteer["id"])
            ],
        }
        for volunteer in pending
    ]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "schema": VolunteerFrontendRegistrationResponse.model_json_schema()
                }
            }
        }
    },
)
async def create_new_volunteer(request: Request):
    """Registra una solicitud pendiente (JSON frontend o multipart legacy)."""

    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            raw_payload = await request.json()
            payload = VolunteerFrontendCreate.model_validate(raw_payload)
        except (
            json.JSONDecodeError,
            UnicodeDecodeError,
            ValidationError,
        ) as exc:
            return _error_response(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Datos de registro no válidos",
                str(exc),
            )

        return services.register_volunteer_from_frontend(payload)

    form = await request.form()

    try:
        volunteer_data = VolunteerCreate(
            nombre=form.get("nombre"),
            contacto=form.get("contacto"),
            habilidades=form.get("habilidades"),
            disponibilidad=form.get("disponibilidad") or "inmediata",
        )
    except ValidationError as exc:
        return _error_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Datos de registro no válidos",
            str(exc),
        )

    uploads: list[UploadFile] = []

    for value in form.getlist("documentos"):
        if isinstance(value, UploadFile) and value.filename:
            uploads.append(value)

    try:
        return services.register_volunteer(
            volunteer_data=volunteer_data,
            documents=uploads,
        )
    except InvalidVolunteerDocument as exc:
        return _error_response(
            status.HTTP_400_BAD_REQUEST,
            "Documento no válido",
            str(exc),
        )


@router.get("/{volunteer_id}/aprobar", response_model=VolunteerActionResponse)
def approve_volunteer_from_email(
    volunteer_id: int,
    token: str = Query(...),
):
    """Aprueba una solicitud desde el enlace enviado al administrador."""

    result = services.approve_volunteer(
        volunteer_id,
        admin_token=token,
        via_api=False,
    )
    if result.get("error") == "not_found":
        return _error_response(
            status.HTTP_404_NOT_FOUND,
            "Solicitud no encontrada",
            f"No existe una solicitud válida con el identificador {volunteer_id}.",
        )
    if result.get("error") == "invalid_transition":
        return _error_response(
            status.HTTP_409_CONFLICT,
            "Transición no válida",
            "La solicitud ya no está pendiente de validación.",
        )
    return result


@router.get("/{volunteer_id}/rechazar", response_model=VolunteerActionResponse)
def reject_volunteer_from_email(
    volunteer_id: int,
    token: str = Query(...),
):
    """Rechaza una solicitud desde el enlace enviado al administrador."""

    result = services.reject_volunteer(
        volunteer_id,
        admin_token=token,
        via_api=False,
    )
    if result.get("error") == "not_found":
        return _error_response(
            status.HTTP_404_NOT_FOUND,
            "Solicitud no encontrada",
            f"No existe una solicitud válida con el identificador {volunteer_id}.",
        )
    if result.get("error") == "invalid_transition":
        return _error_response(
            status.HTTP_409_CONFLICT,
            "Transición no válida",
            "La solicitud ya no está pendiente de validación.",
        )
    return result


@router.post(
    "/{volunteer_id}/aprobar",
    response_model=VolunteerActionResponse,
    dependencies=[Depends(requiere_clave_organizador)],
)
def approve_volunteer_from_api(volunteer_id: int):
    """Aprueba una solicitud pendiente usando la clave de organizador."""

    result = services.approve_volunteer(volunteer_id, via_api=True)
    if result.get("error") == "not_found":
        return _error_response(
            status.HTTP_404_NOT_FOUND,
            "Solicitud no encontrada",
            f"No existe una solicitud con el identificador {volunteer_id}.",
        )
    if result.get("error") == "invalid_transition":
        return _error_response(
            status.HTTP_409_CONFLICT,
            "Transición no válida",
            "La solicitud ya no está pendiente de validación.",
        )
    return result


@router.post(
    "/{volunteer_id}/rechazar",
    response_model=VolunteerActionResponse,
    dependencies=[Depends(requiere_clave_organizador)],
)
def reject_volunteer_from_api(volunteer_id: int):
    """Rechaza una solicitud pendiente usando la clave de organizador."""

    result = services.reject_volunteer(volunteer_id, via_api=True)
    if result.get("error") == "not_found":
        return _error_response(
            status.HTTP_404_NOT_FOUND,
            "Solicitud no encontrada",
            f"No existe una solicitud con el identificador {volunteer_id}.",
        )
    if result.get("error") == "invalid_transition":
        return _error_response(
            status.HTTP_409_CONFLICT,
            "Transición no válida",
            "La solicitud ya no está pendiente de validación.",
        )
    return result

@router.patch(
    "/{volunteer_id}",
    response_model=VolunteerFrontendResponse,
    dependencies=[Depends(requiere_clave_organizador)],
)

def update_volunteer_coordination_status(
    volunteer_id: int,
    update: VolunteerCoordinationUpdate,
):
    """Actualiza el estado operativo de coordinación de un voluntario."""

    try:
        updated = update_coordination_status(
            volunteer_id=volunteer_id,
            status=update.status.value,
        )
    except InvalidVolunteerTransition:
        return _error_response(
            status.HTTP_409_CONFLICT,
            "Operación no permitida",
            "Solo los voluntarios aprobados pueden cambiar su estado operativo.",
        )

    if updated is None:
        return _error_response(
            status.HTTP_404_NOT_FOUND,
            "Voluntario no encontrado",
            f"No existe un voluntario aprobado con el identificador {volunteer_id}.",
        )

    return updated


@router.patch("/{volunteer_id}/disponible", response_model=VolunteerResponse)
def update_volunteer_availability(
    volunteer_id: int,
    update: VolunteerAvailabilityUpdate,
    x_volunteer_token: str | None = Header(default=None, alias="X-Volunteer-Token"),
    token: str | None = Query(default=None),
):
    """Permite al voluntario aprobado marcar si está disponible o no."""

    volunteer_token = x_volunteer_token or token
    if volunteer_token is None:
        return _error_response(
            status.HTTP_401_UNAUTHORIZED,
            "Token requerido",
            "Debes enviar X-Volunteer-Token o el parámetro token.",
        )

    try:
        updated = services.update_availability(
            volunteer_id=volunteer_id,
            is_available=update.is_available,
            volunteer_token=volunteer_token,
        )
    except InvalidVolunteerTransition:
        return _error_response(
            status.HTTP_409_CONFLICT,
            "Operación no permitida",
            "Solo los voluntarios aprobados pueden cambiar su disponibilidad.",
        )

    if updated is None:
        return _error_response(
            status.HTTP_404_NOT_FOUND,
            "Voluntario no encontrado",
            "No existe un voluntario aprobado con ese identificador y token.",
        )

    return updated
