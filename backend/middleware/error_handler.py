"""Manejo centralizado de errores de la API de Nexo.

Este archivo permite que todos los módulos devuelvan los errores con el
mismo formato JSON:

{
    "error": "Nombre del error",
    "detalle": "Explicación del error"
}
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def registrar_manejadores_de_error(app: FastAPI) -> None:
    """Registra en FastAPI los manejadores de errores comunes de Nexo."""

    @app.exception_handler(RequestValidationError)
    async def error_de_validacion(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Convierte los errores automáticos 422 al formato común de Nexo.

        FastAPI genera un error 422 cuando los datos recibidos no cumplen
        el esquema Pydantic. Por ejemplo:

        - Falta un campo obligatorio.
        - Un tipo o prioridad no está permitido.
        - Una coordenada está fuera de rango.
        - Un campo tiene un tipo de dato incorrecto.

        La petición no llega a ejecutarse en routes.py porque FastAPI la
        rechaza antes. Este manejador transforma su respuesta automática.
        """

        # Obtenemos los nombres de los campos que no han superado
        # la validación de Pydantic.
        campos_invalidos = []

        for error in exc.errors():
            # "loc" indica dónde se encuentra el error.
            # Puede tener una estructura como ("body", "tipo").
            ubicacion = error.get("loc", ())

            # Eliminamos "body" porque no es un campo del formulario.
            partes = [
                str(parte)
                for parte in ubicacion
                if parte not in {"body", "query", "path"}
            ]

            if partes:
                nombre_campo = ".".join(partes)

                # Evitamos repetir un campo si contiene varios errores.
                if nombre_campo not in campos_invalidos:
                    campos_invalidos.append(nombre_campo)

        # Creamos una explicación sencilla para quien consume la API.
        if campos_invalidos:
            detalle = (
                "Revisa los siguientes campos: " + ", ".join(campos_invalidos) + "."
            )
        else:
            detalle = "Los datos enviados no cumplen el formato esperado."

        return JSONResponse(
            status_code=422,
            content={
                "error": "Error de validación",
                "detalle": detalle,
            },
        )

    @app.exception_handler(Exception)
    async def excepcion_no_controlada(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Devuelve los errores internos con el formato común de Nexo."""

        return JSONResponse(
            status_code=500,
            content={
                "error": "Error interno de Nexo",
                "detalle": str(exc),
            },
        )
