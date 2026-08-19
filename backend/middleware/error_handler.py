"""Manejo centralizado de errores — parte de la base común, para que
todos los módulos devuelvan errores con el mismo formato."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def registrar_manejadores_de_error(app: FastAPI):
    @app.exception_handler(Exception)
    async def excepcion_no_controlada(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "Error interno de Nexo", "detalle": str(exc)},
        )
