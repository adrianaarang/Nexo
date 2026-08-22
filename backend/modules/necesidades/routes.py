"""Endpoints del mapa de necesidades en tiempo real (Equipo 1, núcleo).

Router mínimo de la base común, para que la app arranque desde el
primer día. TODO (Equipo 1): añadir los endpoints reales
(listar, crear, actualizar estado) usando models.py y schemas.py.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/necesidades", tags=["necesidades"])

# TODO: @router.get(""), @router.post(""), @router.patch("/{id}/estado")
