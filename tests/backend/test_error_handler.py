"""Tests del manejador global de errores de validación de Nexo.

Estas pruebas comprueban que los errores 422 generados automáticamente
por FastAPI utilizan el formato JSON común del proyecto.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from middleware.error_handler import registrar_manejadores_de_error


class ValidationPayload(BaseModel):
    """Datos utilizados para provocar un error de validación."""

    cantidad: int


# Creamos una aplicación pequeña para probar solamente el manejador
# de errores, sin depender de la base de datos ni del resto de Nexo.
validation_app = FastAPI()

# Registramos en la aplicación de prueba los mismos manejadores de errores
# que utiliza la aplicación real.
registrar_manejadores_de_error(validation_app)


@validation_app.post("/test-validacion")
def recibir_datos(
    datos: ValidationPayload,
) -> ValidationPayload:
    """Endpoint de prueba que exige que cantidad sea un número entero."""

    return datos


# TestClient permite realizar peticiones a la aplicación de prueba sin
# tener que arrancar manualmente Uvicorn.
client = TestClient(validation_app)


def test_validation_error_uses_common_format() -> None:
    """Un error 422 debe utilizar las claves error y detalle."""

    # Enviamos texto en un campo que exige un número entero.
    # Esto provoca intencionadamente un error 422 de FastAPI.
    response = client.post(
        "/test-validacion",
        json={"cantidad": "esto no es un número"},
    )

    # Comprobamos que se conserva el código propio de validación.
    assert response.status_code == 422

    # Comprobamos que el cuerpo utiliza el formato común de Nexo.
    assert response.json() == {
        "error": "Error de validación",
        "detalle": "Revisa los siguientes campos: cantidad.",
    }
