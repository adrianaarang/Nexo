"""Operaciones de persistencia SQLite del módulo de personas.

La validación de entrada corresponde a ``schemas.py``. Este módulo ejecuta
consultas parametrizadas y devuelve diccionarios serializables.
"""
from sqlite3 import Row
from typing import Any

from db.database import get_cursor
from modules.personas.schemas import PersonStatus


def _row_to_dict(row: Row | None) -> dict[str, Any] | None:
    """Convierte una fila SQLite en diccionario sin exponer el cursor."""

    return dict(row) if row is not None else None


def mark_person_safe(person_id: int) -> dict[str, Any] | None:
    """Marca como segura una persona ya registrada.

    Devuelve ``None`` si el identificador no existe.

    Repetir la operación cuando la persona ya está en ``estoy_bien`` es
    válido y devuelve el registro sin modificarlo. Esto mantiene la operación
    idempotente y facilita futuros reintentos de sincronización offline.

    Las reglas completas de transición entre estados quedan fuera de esta
    función por ahora, hasta que el Equipo 4 las acuerde.
    """

    with get_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM personas WHERE id = ?",
            (person_id,),
        )
        current_row = cursor.fetchone()

        if current_row is None:
            return None

        if current_row["estado"] == PersonStatus.SAFE.value:
            return dict(current_row)

        cursor.execute(
            "UPDATE personas SET estado = ? WHERE id = ?",
            (PersonStatus.SAFE.value, person_id),
        )

        cursor.execute(
            "SELECT * FROM personas WHERE id = ?",
            (person_id,),
        )
        return _row_to_dict(cursor.fetchone())
