"""Operaciones de persistencia SQLite del módulo de alertas del gestor.

La validación de entrada corresponde a ``schemas.py``. Este módulo solo
ejecuta consultas parametrizadas y devuelve diccionarios serializables.

Las alertas externas (GDACS / Protección Civil) no se persisten aquí: se
obtienen en vivo desde ``services.py``. Esta tabla cubre únicamente las
alertas creadas por el gestor (activación de crisis, nivel de riesgo, zona).
"""
import json
from sqlite3 import Row
from typing import Any, Optional

from db.database import get_cursor
from modules.alertas.schemas import AlertCreate, AlertUpdate


class AlertNotFound(LookupError):
    """Permite que la capa de rutas traduzca un id inexistente a HTTP 404."""


def _row_to_dict(row: Row | None) -> dict[str, Any] | None:
    """Convierte una fila SQLite en diccionario sin exponer el cursor."""

    return dict(row) if row is not None else None


def create_alert(data: AlertCreate) -> dict[str, Any]:
    """Guarda una alerta del gestor validada y devuelve el registro completo."""

    zona_json = json.dumps(data.zona, ensure_ascii=False) if data.zona else "{}"

    with get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO alertas
               (nivel_riesgo, zona, activa, gestor_token, titulo, descripcion, tipo, fuente)
               VALUES (?, ?, 0, ?, ?, ?, ?, 'gestor')""",
            (
                data.nivel_riesgo.value,
                zona_json,
                data.gestor_token,
                data.titulo,
                data.descripcion,
                data.tipo.value if data.tipo else None,
            ),
        )
        alert_id = cursor.lastrowid
        cursor.execute("SELECT * FROM alertas WHERE id = ?", (alert_id,))
        return dict(cursor.fetchone())


def get_alert(alert_id: int) -> dict[str, Any] | None:
    """Devuelve una alerta por id o ``None`` si no existe."""

    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM alertas WHERE id = ?", (alert_id,))
        return _row_to_dict(cursor.fetchone())


def list_alerts() -> list[dict[str, Any]]:
    """Lista todas las alertas del gestor en orden descendente por id."""

    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM alertas ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]


def update_alert(alert_id: int, data: AlertUpdate) -> dict[str, Any] | None:
    """Actualiza campos editables de una alerta. Idempotente por campo.

    Un identificador inexistente se representa con ``None``.
    """

    current = get_alert(alert_id)
    if current is None:
        return None

    nivel = data.nivel_riesgo.value if data.nivel_riesgo is not None else current["nivel_riesgo"]
    zona = (
        json.dumps(data.zona, ensure_ascii=False)
        if data.zona is not None
        else current["zona"]
    )
    titulo = data.titulo if data.titulo is not None else current["titulo"]
    descripcion = data.descripcion if data.descripcion is not None else current["descripcion"]
    tipo = data.tipo.value if data.tipo is not None else current.get("tipo")
    activa = data.activa if data.activa is not None else current["activa"]

    with get_cursor() as cursor:
        cursor.execute(
            """UPDATE alertas
               SET nivel_riesgo = ?, zona = ?, titulo = ?, descripcion = ?, tipo = ?, activa = ?
               WHERE id = ?""",
            (nivel, zona, titulo, descripcion, tipo, int(activa), alert_id),
        )
        cursor.execute("SELECT * FROM alertas WHERE id = ?", (alert_id,))
        return dict(cursor.fetchone())


def set_activation(
    alert_id: int,
    activa: bool,
    alto_riesgo: bool = False,
) -> dict[str, Any] | None:
    """Activa/desactiva una alerta. Si ``alto_riesgo`` es True, fija nivel='alto'.

    Repetir el mismo estado es idempotente. Id inexistente -> ``None``.
    """

    current = get_alert(alert_id)
    if current is None:
        return None

    nivel = "alto" if alto_riesgo else current["nivel_riesgo"]

    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE alertas SET activa = ?, nivel_riesgo = ? WHERE id = ?",
            (int(activa), nivel, alert_id),
        )
        cursor.execute("SELECT * FROM alertas WHERE id = ?", (alert_id,))
        return dict(cursor.fetchone())


def delete_alert(alert_id: int) -> bool:
    """Elimina una alerta del gestor. Devuelve True si existía y se borró."""

    with get_cursor() as cursor:
        cursor.execute("DELETE FROM alertas WHERE id = ?", (alert_id,))
        return cursor.rowcount > 0
