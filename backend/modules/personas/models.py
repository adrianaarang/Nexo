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


def get_all_personas(
    search_q: str | None = None,
) -> list[dict[str, Any]]:
    """Consulta y retorna todas las personas activas."""

    with get_cursor() as cursor:
        query = """
            SELECT *
            FROM personas
            WHERE is_deleted = 0
        """
        params: list[Any] = []

        if search_q:
            query += """
                AND (
                    nombre LIKE ?
                    OR ultima_ubicacion LIKE ?
                )
            """
            params.extend(
                [
                    f"%{search_q}%",
                    f"%{search_q}%",
                ]
            )

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]


def get_persona_by_id(
    person_id: int,
) -> dict[str, Any] | None:
    """Busca y devuelve una persona activa por su ID."""

    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM personas
            WHERE id = ?
            AND is_deleted = 0
            """,
            (person_id,),
        )

        return _row_to_dict(cursor.fetchone())


def create_persona(
    data: dict[str, Any],
) -> dict[str, Any] | None:
    """Inserta una nueva persona y retorna el registro creado."""

    with get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO personas (
                nombre,
                edad,
                ultima_ubicacion,
                descripcion,
                estado,
                reportado_por,
                client_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("nombre"),
                data.get("edad"),
                data.get("ultima_ubicacion"),
                data.get("descripcion"),
                data.get(
                    "estado",
                    PersonStatus.MISSING.value,
                ),
                data.get("reportado_por"),
                data.get("client_id"),
            ),
        )

        new_id = cursor.lastrowid

        if new_id is None:
            return None

        return get_persona_by_id(new_id)


def mark_person_safe(
    person_id: int,
) -> dict[str, Any] | None:
    """Marca como segura una persona e incrementa su versión."""

    current_person = get_persona_by_id(person_id)

    if current_person is None:
        return None

    # La operación es idempotente.
    if current_person.get("estado") == PersonStatus.SAFE.value:
        return current_person

    with get_cursor() as cursor:
        cursor.execute(
            """
            UPDATE personas
            SET
                estado = ?,
                version = version + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            AND is_deleted = 0
            """,
            (
                PersonStatus.SAFE.value,
                person_id,
            ),
        )

    return get_persona_by_id(person_id)