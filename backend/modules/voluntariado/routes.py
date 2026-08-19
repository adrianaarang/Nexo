"""Endpoints de voluntariado (Equipo 3, núcleo).

Router mínimo de la base común. TODO (Equipo 3): añadir listar/crear
voluntarios usando models.py y schemas.py.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/voluntarios", tags=["voluntariado"])

# TODO: @router.get(""), @router.post("")
