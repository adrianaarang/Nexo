"""Operaciones de persistencia SQLite del módulo de voluntariado.

La validación de entrada corresponde a ``schemas.py``. Este módulo solo
ejecuta consultas parametrizadas y devuelve diccionarios serializables.
"""
from sqlite3 import Row
from typing import Any

from db.database import get_cursor
from modules.voluntariado.schemas import VolunteerStatus


class InvalidVolunteerTransition(ValueError):
    """Permite que la capa de rutas traduzca una transición inválida a HTTP 409."""


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


def list_volunteers(
    skill: str | None = None,
    is_available: bool | None = None,
) -> list[dict[str, Any]]:
    """Lista voluntarios aprobados con filtros opcionales."""

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


def list_pending_volunteers() -> list[dict[str, Any]]:
    """Lista solicitudes pendientes de validación administrativa."""

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

    with get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO voluntarios
               (nombre, contacto, habilidades, disponibilidad,
                estado, disponible, admin_token, volunteer_token)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                name,
                contact,
                skills,
                availability,
                VolunteerStatus.PENDING.value,
                0,
                admin_token,
                volunteer_token,
            ),
        )
        volunteer_id = cursor.lastrowid
        cursor.execute(
            "SELECT * FROM voluntarios WHERE id = ?",
            (volunteer_id,),
        )
        return _public_volunteer_row(dict(cursor.fetchone()))


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
               SET estado = ?, disponible = ?, admin_token = ''
               WHERE id = ?""",
            (VolunteerStatus.APPROVED.value, 1, volunteer_id),
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
