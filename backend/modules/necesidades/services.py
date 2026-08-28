"""Reglas de negocio y fachada pública del módulo de necesidades."""

from typing import Any

from modules.necesidades import models
from modules.necesidades.schemas import NeedCreate, NeedStatus, NeedType


def list_needs(
    status: NeedStatus | None = None,
    need_type: NeedType | None = None,
) -> list[dict[str, Any]]:
    """Lista necesidades aplicando los filtros públicos del módulo."""

    return models.list_needs(status=status, need_type=need_type)


def get_need(need_id: int) -> dict[str, Any] | None:
    """Devuelve una necesidad por identificador."""

    return models.get_need(need_id)


def create_need(need: NeedCreate) -> dict[str, Any]:
    """Completa los valores derivados y guarda una necesidad."""

    if not need.title:
        need = need.model_copy(
            update={"title": f"Necesidad de {need.need_type.value}"}
        )
    return models.create_need(need)


def update_need_status(
    need_id: int,
    status: NeedStatus,
) -> dict[str, Any] | None:
    """Actualiza el estado respetando las transiciones del modelo."""

    return models.update_need_status(need_id, status)


__all__ = ["create_need", "get_need", "list_needs", "update_need_status"]
