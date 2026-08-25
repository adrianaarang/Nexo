"""Endpoint de alertas oficiales (Equipo 2, núcleo).

Router mínimo de la base común. TODO (Equipo 2): añadir el endpoint
GET que llama a services.py (GDACS + Protección Civil).
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/alertas", tags=["alertas"])

# TODO: @router.get("")
