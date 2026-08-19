"""Sincronización del modo offline (Equipo 4, siguiente prioridad).

Router mínimo de la base común. TODO (Equipo 4): recibir las acciones
guardadas offline por el frontend (ver
frontend/js/siguiente/modo-offline/syncQueue.js) y aplicarlas sobre los
modelos de cada módulo (necesidades, voluntariado, donaciones, personas).
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/sync", tags=["sync"])

# TODO: @router.post("")
