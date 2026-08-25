"""Autenticación mínima — placeholder de la base común.

En esta fase Nexo no requiere login para reportar necesidades o
apuntarse como voluntario (baja fricción es clave en una emergencia).
Queda preparado por si algún equipo necesita proteger una acción
sensible más adelante.
"""
from fastapi import Header, HTTPException

from config import NEXO_ADMIN_KEY


def requiere_clave_organizador(x_nexo_key: str | None = Header(default=None)):
    """Úsalo como dependencia en rutas sensibles:
    `@router.delete(..., dependencies=[Depends(requiere_clave_organizador)])`
    """
    if x_nexo_key is None:
        raise HTTPException(status_code=401, detail="Falta cabecera X-Nexo-Key")
    if x_nexo_key != NEXO_ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Clave de organizador no válida")
