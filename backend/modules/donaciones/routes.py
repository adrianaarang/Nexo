"""Endpoints de donaciones (Equipo 3, núcleo).

Router mínimo de la base común. TODO (Equipo 3): añadir listar/crear
donaciones usando models.py.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/donaciones", tags=["donaciones"])

# TODO: @router.get(""), @router.post("")
