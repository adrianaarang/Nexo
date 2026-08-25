"""Endpoints de registro de personas (Equipo 4, siguiente prioridad).

Este módulo recibe las peticiones HTTP relacionadas con personas. El acceso
a la base de datos se delega en ``models.py`` y la validación de entrada y
salida en ``schemas.py``.

El listado y el registro general de personas siguen pendientes de la pareja
responsable de Registro de Personas.
"""
from fastapi import APIRouter,  Query,status
from fastapi.responses import JSONResponse

from modules.personas import models
from modules.personas.schemas import (
    PersonCreate,
    PersonResponse,
    PersonSafeRequest
)  


router = APIRouter(
    prefix="/api/personas",
    tags=["personas"],
)

@router.get("/", response_model=list[PersonResponse])
def list_personas(q: str | None = Query(None)):
    """Obtiene el listado de personas activas con opción de filtro por búsqueda"""
    return models.get_all_personas(search_q=q)

@router.get(
    "/{persona_id}",
    response_model=PersonResponse,
    responses = {
        status.HTTP_404_NOT_FOUND: {
            "description": "Persona no encontrada",
            "content":{
                "application/json":{
                    "example":{
                        "error": "Persona no encontrada",
                        "detalle": "No existe una persona con el identificador 999"
                    }
                }
            }
        }
    }
)

def get_persona(persona_id: int):
    """Obtiene la información detallada de una persona por su identificador"""
    person = models.get_persona_by_id(person_id)
    if person is None:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content ={
                "error": "Persona no encontrada",
                "detalle": "No existe una persona con el identificador {persona_id}"
            },
        )
    return person

@router.post(
    "/",
    response_model = PersonResponse,
    status_code = status.HTTP_201_CREATED,
)

def create_persona(payload: PersonCreate):
    """Registra una nueva persona en el sistema"""
    return models.create_persona(payload.model_dump(by_alias = True))

@router.post(
    "/estoy-bien",
    response_model=PersonResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Persona no encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Persona no encontrada",
                        "detalle": "No existe una persona con el identificador 999"
                    }
                }
            },
        },
    },
)
def mark_safe(request: PersonSafeRequest):
    """Marca como segura una persona previamente registrada.

    La operación recibe el identificador de una persona existente y delega
    en ``models.py`` el cambio de estado a ``estoy_bien``.

    Repetir la misma operación es válido e idempotente.
    """

    person = models.mark_person_safe(request.person_id)

    if person is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Persona no encontrada",
                "detalle": (
                    f"No existe una persona con el identificador "
                    f"{request.person_id}."
                ),
            },
        )

    return person
