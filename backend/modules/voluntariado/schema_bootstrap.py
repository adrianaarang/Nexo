"""Bootstrap idempotente del esquema de voluntarios.

Solo modifica la tabla ``voluntarios``. No usa ``db/migrations/`` ni
``init_db()``. Pensado para ejecutarse una vez por proceso desde ``models.py``.
"""
import sqlite3

from db.database import get_cursor

_VOLUNTEER_COLUMNS: tuple[tuple[str, str], ...] = (
    ("first_name", "TEXT NOT NULL DEFAULT ''"),
    ("last_name", "TEXT NOT NULL DEFAULT ''"),
    ("dni", "TEXT NOT NULL DEFAULT ''"),
    ("birth_date", "TEXT NOT NULL DEFAULT ''"),
    ("phone", "TEXT NOT NULL DEFAULT ''"),
    ("locality", "TEXT NOT NULL DEFAULT ''"),
    ("tasks", "TEXT NOT NULL DEFAULT '[]'"),
    ("certifications", "TEXT NOT NULL DEFAULT '[]'"),
    ("transportation", "TEXT NOT NULL DEFAULT ''"),
    ("vehicle_type", "TEXT"),
    ("availability_slots", "TEXT NOT NULL DEFAULT '[]'"),
    (
        "coordination_status",
        "TEXT NOT NULL DEFAULT 'available' "
        "CHECK (coordination_status IN ('available', 'assigned', 'resting'))",
    ),
)

_BACKFILL_STATEMENTS: tuple[str, ...] = (
    """
    UPDATE voluntarios SET
      first_name = trim(substr(nombre, 1, instr(nombre || ' ', ' ') - 1)),
      last_name = trim(substr(nombre, instr(nombre || ' ', ' ') + 1))
    WHERE (first_name IS NULL OR first_name = '')
      AND (last_name IS NULL OR last_name = '')
      AND trim(nombre) != ''
    """,
    """
    UPDATE voluntarios SET phone = contacto
    WHERE (phone IS NULL OR phone = '') AND trim(contacto) != ''
    """,
    """
    UPDATE voluntarios SET coordination_status = CASE
      WHEN disponible = 1 THEN 'available' ELSE 'resting' END
    WHERE estado = 'aprobado'
      AND (dni IS NULL OR dni = '')
      AND coordination_status = 'available'
    """,
)


def _existing_columns(cursor: sqlite3.Cursor) -> set[str]:
    cursor.execute("PRAGMA table_info(voluntarios)")
    return {row[1] for row in cursor.fetchall()}


def _add_column_if_missing(
    cursor: sqlite3.Cursor,
    column_name: str,
    column_definition: str,
    existing: set[str],
) -> None:
    if column_name in existing:
        return
    try:
        cursor.execute(
            f"ALTER TABLE voluntarios ADD COLUMN {column_name} {column_definition}"
        )
        existing.add(column_name)
    except sqlite3.OperationalError as exc:
        if "duplicate column name" in str(exc).lower():
            existing.update(_existing_columns(cursor))
            return
        raise


def ensure_voluntariado_schema() -> None:
    """Añade columnas frontend a ``voluntarios`` y rellena filas legacy."""

    with get_cursor() as cursor:
        existing = _existing_columns(cursor)
        for column_name, column_definition in _VOLUNTEER_COLUMNS:
            _add_column_if_missing(cursor, column_name, column_definition, existing)
        for statement in _BACKFILL_STATEMENTS:
            cursor.execute(statement)
