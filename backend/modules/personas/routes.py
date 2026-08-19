"""Endpoints de registro de personas (Equipo 4, siguiente prioridad).

Router mínimo de la base común. TODO (Equipo 4): añadir listar/crear
personas y el endpoint de "estoy bien", usando models.py y schemas.py.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/personas", tags=["personas"])

# TODO: @router.get(""), @router.post(""), @router.post("/estoy-bien")
