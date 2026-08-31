"""Operaciones de persistencia SQLite del módulo de necesidades.

La validación de entrada corresponde a ``schemas.py``. Este módulo solo
ejecuta consultas parametrizadas y devuelve diccionarios serializables.
"""
from sqlite3 import Row
from typing import Any

from db.database import get_cursor
from modules.necesidades.schemas import NeedCreate, NeedStatus, NeedType


class InvalidStatusTransition(ValueError):
    """Permite que la capa de rutas traduzca una transición inválida a HTTP 409."""


# Ciclo de vida simplificado a un solo paso: una necesidad solo puede pasar
# de abierta a cubierta; no hay estados intermedios ni se puede reabrir.
STATUS_TRANSITIONS = {
    NeedStatus.OPEN: NeedStatus.COVERED,
}


def _row_to_dict(row: Row | None) -> dict[str, Any] | None:
    """Convierte una fila SQLite en diccionario sin exponer el cursor."""

    return dict(row) if row is not None else None


def list_needs(
    status: NeedStatus | None = None,
    need_type: NeedType | None = None,
) -> list[dict[str, Any]]:
    """Lista necesidades en orden estable y permite filtrar por estado o tipo."""

    # Solo se construye dinámicamente la estructura de WHERE. Los valores
    # recibidos siguen siendo parámetros y nunca se interpretan como SQL.
    conditions: list[str] = []
    parameters: list[str] = []

    if status is not None:
        conditions.append("estado = ?")
        parameters.append(status.value)
    if need_type is not None:
        conditions.append("tipo = ?")
        parameters.append(need_type.value)

    query = "SELECT * FROM necesidades"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY id ASC"

    with get_cursor() as cursor:
        cursor.execute(query, parameters)
        return [dict(row) for row in cursor.fetchall()]


def get_need(need_id: int) -> dict[str, Any] | None:
    """Devuelve una necesidad por id o ``None`` si no existe."""

    with get_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM necesidades WHERE id = ?",
            (need_id,),
        )
        return _row_to_dict(cursor.fetchone())


def create_need(need: NeedCreate) -> dict[str, Any]:
    """Guarda una necesidad validada y devuelve el registro completo."""

    with get_cursor() as cursor:
        # SQLite genera el id, el estado inicial y la fecha de creación.
        cursor.execute(
            """INSERT INTO necesidades
               (titulo, tipo, descripcion, direccion, latitud, longitud, prioridad)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                need.title,
                need.need_type.value,
                need.description,
                need.address,
                need.latitude,
                need.longitude,
                need.priority.value,
            ),
        )
        need_id = cursor.lastrowid

        # La misma conexión permite leer también los datos generados por SQLite.
        cursor.execute(
            "SELECT * FROM necesidades WHERE id = ?",
            (need_id,),
        )
        return dict(cursor.fetchone())


def update_need_status(
    need_id: int,
    status: NeedStatus,
) -> dict[str, Any] | None:
    """Avanza el estado sin permitir saltos ni reabrir registros.

    Repetir el estado actual es válido para que los reintentos del cliente sean
    idempotentes. Un identificador inexistente se representa con ``None``.
    """

    with get_cursor() as cursor:
        # Se lee primero para distinguir un registro inexistente de una
        # transición de negocio inválida en la capa de rutas.
        cursor.execute(
            "SELECT * FROM necesidades WHERE id = ?",
            (need_id,),
        )
        current_row = cursor.fetchone()
        if current_row is None:
            return None

        current_status = NeedStatus(current_row["estado"])
        if status == current_status:
            return dict(current_row)

        if STATUS_TRANSITIONS.get(current_status) != status:
            raise InvalidStatusTransition(
                f"Cannot change status from {current_status.value} to {status.value}"
            )

        cursor.execute(
            "UPDATE necesidades SET estado = ? WHERE id = ?",
            (status.value, need_id),
        )

        # Se devuelve la representación persistida que espera la respuesta API.
        cursor.execute(
            "SELECT * FROM necesidades WHERE id = ?",
            (need_id,),
        )
        return _row_to_dict(cursor.fetchone())
