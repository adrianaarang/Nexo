"""Operaciones de persistencia SQLite del módulo de voluntariado.

La validación de entrada corresponde a ``schemas.py``. Este módulo solo
ejecuta consultas parametrizadas y devuelve diccionarios serializables.
"""
import json
from sqlite3 import Row
from typing import Any

from db.database import get_cursor
from modules.voluntariado.schema_bootstrap import ensure_voluntariado_schema
from modules.voluntariado.schemas import (
    CoordinationStatus,
    VolunteerFrontendCreate,
    VolunteerStatus,
)

_schema_ready = False


class InvalidVolunteerTransition(ValueError):
    """Permite que la capa de rutas traduzca una transición inválida a HTTP 409."""


def _ensure_schema() -> None:
    global _schema_ready
    if not _schema_ready:
        ensure_voluntariado_schema()
        _schema_ready = True


def _row_to_dict(row: Row | None) -> dict[str, Any] | None:
    """Convierte una fila SQLite en diccionario sin exponer el cursor."""

    return dict(row) if row is not None else None


def _normalize_volunteer_row(row: dict[str, Any]) -> dict[str, Any]:
    """Adapta columnas SQLite al contrato JSON de la API."""

    normalized = dict(row)
    normalized["disponible"] = bool(normalized.get("disponible", 0))
    return normalized


def _public_volunteer_row(row: dict[str, Any]) -> dict[str, Any]:
    """Elimina tokens internos antes de serializar una respuesta pública."""

    public_row = _normalize_volunteer_row(row)
    public_row.pop("admin_token", None)
    public_row.pop("volunteer_token", None)
    return public_row


def _loads_json_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []
    return parsed if isinstance(parsed, list) else []


def _split_legacy_name(nombre: str) -> tuple[str, str]:
    cleaned = nombre.strip()
    if not cleaned:
        return "", ""
    if " " not in cleaned:
        return cleaned, ""
    first, _, last = cleaned.partition(" ")
    return first.strip(), last.strip()

def _resolve_coordination_status(row: dict[str, Any]) -> str:
    coordination_status = (row.get("coordination_status") or "").strip()

    if coordination_status in {
        CoordinationStatus.AVAILABLE.value,
        CoordinationStatus.ASSIGNED.value,
        CoordinationStatus.RESTING.value,
    }:
        return coordination_status

    return (
        CoordinationStatus.AVAILABLE.value
        if bool(row.get("disponible", 0))
        else CoordinationStatus.RESTING.value
    )


def _to_frontend_dict(row: dict[str, Any]) -> dict[str, Any]:
    """Mapea una fila de BD al contrato JSON del frontend."""

    first_name = (row.get("first_name") or "").strip()
    last_name = (row.get("last_name") or "").strip()
    if not first_name and not last_name:
        first_name, last_name = _split_legacy_name(row.get("nombre") or "")

    full_name = f"{first_name} {last_name}".strip() or (row.get("nombre") or "").strip()
    skills = (row.get("habilidades") or "").strip()
    if row.get("skills"):
        skills = str(row.get("skills")).strip() or skills

    availability_slots = []
    for slot in _loads_json_list(row.get("availability_slots")):
        if isinstance(slot, dict) and slot.get("starts_at"):
            availability_slots.append({"starts_at": slot["starts_at"]})

    vehicle_type = row.get("vehicle_type")
    if vehicle_type == "":
        vehicle_type = None

    return {
        "id": row["id"],
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "locality": (row.get("locality") or "").strip(),
        "tasks": [str(task) for task in _loads_json_list(row.get("tasks"))],
        "certifications": [
            str(certification)
            for certification in _loads_json_list(row.get("certifications"))
        ],
        "transportation": (row.get("transportation") or "").strip(),
        "vehicle_type": vehicle_type,
        "availability_slots": availability_slots,
        "skills": skills,
        "status": _resolve_coordination_status(row),
    }


def _availability_summary(slots: list[dict[str, str]]) -> str:
    if not slots:
        return "inmediata"
    return f"{len(slots)} franjas indicadas"


def _disponible_for_status(status: str) -> int:
    return 1 if status == CoordinationStatus.AVAILABLE.value else 0


def list_volunteers(
    skill: str | None = None,
    is_available: bool | None = None,
) -> list[dict[str, Any]]:
    """Lista voluntarios aprobados con filtros opcionales."""

    _ensure_schema()
    conditions = ["estado = ?"]
    parameters: list[Any] = [VolunteerStatus.APPROVED.value]

    if skill is not None:
        conditions.append("LOWER(habilidades) LIKE ?")
        parameters.append(f"%{skill.strip().lower()}%")
    if is_available is not None:
        conditions.append("disponible = ?")
        parameters.append(1 if is_available else 0)

    query = "SELECT * FROM voluntarios WHERE " + " AND ".join(conditions)
    query += " ORDER BY id ASC"

    with get_cursor() as cursor:
        cursor.execute(query, parameters)
        return [_public_volunteer_row(dict(row)) for row in cursor.fetchall()]


def list_volunteers_for_frontend(
    coordination_status: str | None = None,
    skill: str | None = None,
    is_available: bool | None = None,
) -> list[dict[str, Any]]:
    """Lista voluntarios aprobados en el contrato del frontend."""

    _ensure_schema()
    conditions = ["estado = ?"]
    parameters: list[Any] = [VolunteerStatus.APPROVED.value]

    if skill is not None:
        conditions.append("LOWER(habilidades) LIKE ?")
        parameters.append(f"%{skill.strip().lower()}%")
        
    if is_available is not None:
        conditions.append("disponible = ?")
        parameters.append(1 if is_available else 0)
    
    if coordination_status is not None:
        conditions.append("coordination_status = ?")
        parameters.append(coordination_status)

    query = "SELECT * FROM voluntarios WHERE " + " AND ".join(conditions)
    query += " ORDER BY id ASC"

    with get_cursor() as cursor:
        cursor.execute(query, parameters)
        rows = [dict(row) for row in cursor.fetchall()]

    volunteers = [_to_frontend_dict(row) for row in rows]
    if coordination_status is None:
        return volunteers
    return [
        volunteer
        for volunteer in volunteers
        if volunteer["status"] == coordination_status
    ]


def list_pending_volunteers() -> list[dict[str, Any]]:
    """Lista solicitudes pendientes de validación administrativa."""

    _ensure_schema()
    with get_cursor() as cursor:
        cursor.execute(
            """SELECT * FROM voluntarios
               WHERE estado = ?
               ORDER BY id ASC""",
            (VolunteerStatus.PENDING.value,),
        )
        return [_public_volunteer_row(dict(row)) for row in cursor.fetchall()]


def get_volunteer(volunteer_id: int) -> dict[str, Any] | None:
    """Devuelve un voluntario por id o ``None`` si no existe."""

    _ensure_schema()
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM voluntarios WHERE id = ?",
            (volunteer_id,),
        )
        row = _row_to_dict(cursor.fetchone())
        return _normalize_volunteer_row(row) if row is not None else None


def get_volunteer_by_admin_token(
    volunteer_id: int,
    token: str,
) -> dict[str, Any] | None:
    """Devuelve un voluntario si el token administrativo coincide."""

    _ensure_schema()
    with get_cursor() as cursor:
        cursor.execute(
            """SELECT * FROM voluntarios
               WHERE id = ? AND admin_token = ?""",
            (volunteer_id, token),
        )
        row = _row_to_dict(cursor.fetchone())
        return _normalize_volunteer_row(row) if row is not None else None


def get_volunteer_by_volunteer_token(
    volunteer_id: int,
    token: str,
) -> dict[str, Any] | None:
    """Devuelve un voluntario si el token del propio voluntario coincide."""

    _ensure_schema()
    with get_cursor() as cursor:
        cursor.execute(
            """SELECT * FROM voluntarios
               WHERE id = ? AND volunteer_token = ?""",
            (volunteer_id, token),
        )
        row = _row_to_dict(cursor.fetchone())
        return _normalize_volunteer_row(row) if row is not None else None


def create_volunteer_pending(
    name: str,
    contact: str,
    skills: str,
    availability: str,
    admin_token: str,
    volunteer_token: str,
) -> dict[str, Any]:
    """Guarda una solicitud pendiente y devuelve el registro completo."""

    _ensure_schema()
    with get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO voluntarios
               (nombre, contacto, habilidades, disponibilidad,
                estado, disponible, admin_token, volunteer_token,
                coordination_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                name,
                contact,
                skills,
                availability,
                VolunteerStatus.PENDING.value,
                0,
                admin_token,
                volunteer_token,
                CoordinationStatus.AVAILABLE.value,
            ),
        )
        volunteer_id = cursor.lastrowid
        cursor.execute(
            "SELECT * FROM voluntarios WHERE id = ?",
            (volunteer_id,),
        )
        return _public_volunteer_row(dict(cursor.fetchone()))


def _to_frontend_registration_dict(row: dict[str, Any]) -> dict[str, Any]:
    payload = _to_frontend_dict(row)
    payload.update(
        {
            "dni": (row.get("dni") or "").strip(),
            "birth_date": (row.get("birth_date") or "").strip(),
            "phone": (row.get("phone") or row.get("contacto") or "").strip(),
        }
    )
    return payload


def create_volunteer_pending_from_frontend(
    data: VolunteerFrontendCreate,
    admin_token: str,
    volunteer_token: str,
) -> dict[str, Any]:
    """Guarda una solicitud pendiente enviada desde el formulario frontend."""

    _ensure_schema()
    legacy_name = f"{data.first_name} {data.last_name}".strip()
    legacy_skills = (data.skills or "").strip()
    availability_slots = [
    {"starts_at": slot.starts_at.isoformat()}
    for slot in data.availability_slots
    ]
    availability = _availability_summary(availability_slots)

    with get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO voluntarios
               (nombre, contacto, habilidades, disponibilidad,
                estado, disponible, admin_token, volunteer_token,
                first_name, last_name, dni, birth_date, phone, locality,
                tasks, certifications, transportation, vehicle_type,
                availability_slots, coordination_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                legacy_name,
                data.phone,
                legacy_skills,
                availability,
                VolunteerStatus.PENDING.value,
                0,
                admin_token,
                volunteer_token,
                data.first_name,
                data.last_name,
                data.dni,
                data.birth_date.isoformat(),
                data.phone,
                data.locality,
                json.dumps([task.value for task in data.tasks]),
                json.dumps([cert.value for cert in data.certifications]),
                data.transportation.value,
                data.vehicle_type.value if data.vehicle_type else None,
                json.dumps(availability_slots),
                CoordinationStatus.AVAILABLE.value,
            ),
        )
        volunteer_id = cursor.lastrowid
        cursor.execute(
            "SELECT * FROM voluntarios WHERE id = ?",
            (volunteer_id,),
        )
        row = dict(cursor.fetchone())
        return _to_frontend_registration_dict(row)


def save_volunteer_document(
    volunteer_id: int,
    original_name: str,
    stored_path: str,
    mime_type: str,
) -> dict[str, Any]:
    """Registra un documento adjunto a un voluntario."""

    with get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO voluntario_documentos
               (voluntario_id, nombre_original, ruta, tipo_mime)
               VALUES (?, ?, ?, ?)""",
            (volunteer_id, original_name, stored_path, mime_type),
        )
        document_id = cursor.lastrowid
        cursor.execute(
            "SELECT * FROM voluntario_documentos WHERE id = ?",
            (document_id,),
        )
        return dict(cursor.fetchone())


def get_volunteer_documents(volunteer_id: int) -> list[dict[str, Any]]:
    """Devuelve los documentos asociados a un voluntario."""

    with get_cursor() as cursor:
        cursor.execute(
            """SELECT * FROM voluntario_documentos
               WHERE voluntario_id = ?
               ORDER BY id ASC""",
            (volunteer_id,),
        )
        return [dict(row) for row in cursor.fetchall()]


def approve_volunteer_record(volunteer_id: int) -> dict[str, Any] | None:
    """Marca una solicitud como aprobada e invalida el token administrativo."""

    volunteer = get_volunteer(volunteer_id)
    if volunteer is None:
        return None
    if volunteer["estado"] != VolunteerStatus.PENDING.value:
        raise InvalidVolunteerTransition(
            f"Cannot approve volunteer in status {volunteer['estado']}"
        )

    with get_cursor() as cursor:
        cursor.execute(
            """UPDATE voluntarios
               SET estado = ?, disponible = ?, admin_token = '',
                   coordination_status = ?
               WHERE id = ?""",
            (
                VolunteerStatus.APPROVED.value,
                1,
                CoordinationStatus.AVAILABLE.value,
                volunteer_id,
            ),
        )
        cursor.execute(
            "SELECT * FROM voluntarios WHERE id = ?",
            (volunteer_id,),
        )
        return _normalize_volunteer_row(dict(cursor.fetchone()))


def reject_volunteer_record(volunteer_id: int) -> dict[str, Any] | None:
    """Marca una solicitud como rechazada e invalida el token administrativo."""

    volunteer = get_volunteer(volunteer_id)
    if volunteer is None:
        return None
    if volunteer["estado"] != VolunteerStatus.PENDING.value:
        raise InvalidVolunteerTransition(
            f"Cannot reject volunteer in status {volunteer['estado']}"
        )

    with get_cursor() as cursor:
        cursor.execute(
            """UPDATE voluntarios
               SET estado = ?, disponible = 0, admin_token = ''
               WHERE id = ?""",
            (VolunteerStatus.REJECTED.value, volunteer_id),
        )
        cursor.execute(
            "SELECT * FROM voluntarios WHERE id = ?",
            (volunteer_id,),
        )
        return _normalize_volunteer_row(dict(cursor.fetchone()))


def update_volunteer_availability(
    volunteer_id: int,
    is_available: bool,
) -> dict[str, Any] | None:
    """Actualiza la disponibilidad activa de un voluntario aprobado."""

    volunteer = get_volunteer(volunteer_id)
    if volunteer is None:
        return None
    if volunteer["estado"] != VolunteerStatus.APPROVED.value:
        raise InvalidVolunteerTransition(
            "Only approved volunteers can update availability"
        )

    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE voluntarios SET disponible = ? WHERE id = ?",
            (1 if is_available else 0, volunteer_id),
        )
        cursor.execute(
            "SELECT * FROM voluntarios WHERE id = ?",
            (volunteer_id,),
        )
        return _public_volunteer_row(dict(cursor.fetchone()))


def update_coordination_status(
    volunteer_id: int,
    status: str,
) -> dict[str, Any] | None:
    """Actualiza el estado operativo y sincroniza ``disponible``."""

    volunteer = get_volunteer(volunteer_id)
    if volunteer is None:
        return None
    if volunteer["estado"] != VolunteerStatus.APPROVED.value:
        raise InvalidVolunteerTransition(
            "Only approved volunteers can update coordination status"
        )

    with get_cursor() as cursor:
        cursor.execute(
            """UPDATE voluntarios
               SET coordination_status = ?, disponible = ?
               WHERE id = ?""",
            (status, _disponible_for_status(status), volunteer_id),
        )
        cursor.execute(
            "SELECT * FROM voluntarios WHERE id = ?",
            (volunteer_id,),
        )
        return _to_frontend_dict(dict(cursor.fetchone()))
