"""Capa de servicios del módulo de necesidades.

Concentra las reglas de negocio que no son ni HTTP (routes.py) ni acceso
a datos (models.py). De momento hay una sola regla: cuando el formulario
simplificado no pide título, aquí se genera uno a partir de la categoría
antes de guardar. routes.py llama siempre a este módulo, nunca a models.py
directamente, para que esta regla no se pueda saltar por accidente.
"""

from modules.necesidades.models import InvalidStatusTransition
from modules.necesidades.models import create_need as _create_need
from modules.necesidades.models import get_need as _get_need
from modules.necesidades.models import list_needs as _list_needs
from modules.necesidades.models import update_need_status as _update_need_status
from modules.necesidades.schemas import (
    NEED_TYPE_LABELS,
    NeedCreate,
    NeedStatus,
    NeedType,
)

__all__ = [
    "InvalidStatusTransition",
    "list_needs",
    "get_need",
    "create_need",
    "update_need_status",
]


def _default_title(need_type: NeedType) -> str:
    """Genera un título legible a partir de la categoría (sin el emoji)."""

    etiqueta = NEED_TYPE_LABELS[need_type]
    _emoji, nombre = etiqueta.split(" ", 1)
    return f"Necesidad de {nombre.lower()}"


def list_needs(
    status: NeedStatus | None = None,
    need_type: NeedType | None = None,
):
    """Lista necesidades, con los mismos filtros opcionales que la API pública."""

    return _list_needs(status=status, need_type=need_type)


def get_need(need_id: int):
    """Devuelve una necesidad por id, o ``None`` si no existe."""

    return _get_need(need_id)


def create_need(need: NeedCreate):
    """Rellena el título por defecto cuando el formulario lo deja vacío y guarda."""

    if not need.title.strip():
        need = need.model_copy(update={"title": _default_title(need.need_type)})

    return _create_need(need)


def update_need_status(need_id: int, status: NeedStatus):
    """Avanza el estado de una necesidad (abierta -> cubierta)."""

    return _update_need_status(need_id=need_id, status=status)
