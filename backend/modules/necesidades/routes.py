"""Endpoints del módulo de necesidades.

Este archivo se encarga de recibir las peticiones HTTP relacionadas
con las necesidades del mapa y devolver una respuesta al frontend.

Aquí no escribimos directamente las consultas SQL ni la regla del
título por defecto. Para eso usamos services.py, que a su vez habla
con models.py.
"""

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

# routes.py solo habla con services.py (nunca con models.py directamente),
# para que reglas como "título por defecto" no se puedan saltar por accidente.
from modules.necesidades.services import (
    InvalidStatusTransition,
    create_need,
    get_need,
    list_needs,
    update_need_status,
)

from modules.necesidades.schemas import (
    NeedCreate,
    NeedResponse,
    NeedStatus,
    NeedStatusUpdate,
    NeedType,
)

# Creamos el router específico del módulo de necesidades.
#
# prefix:
# Todas las rutas creadas en este archivo comenzarán automáticamente
# por /api/necesidades.
#
# tags:
# Agrupa estos endpoints dentro de la sección "necesidades"
# en la documentación automática de FastAPI (/docs).
router = APIRouter(
    prefix="/api/necesidades",
    tags=["necesidades"],
)


def _error_necesidad_no_encontrada(need_id: int) -> JSONResponse:
    """Formato único de error {"error", "detalle"} para un id inexistente."""

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Necesidad no encontrada",
            "detalle": f"No existe una necesidad con el identificador {need_id}.",
        },
    )


@router.get("", response_model=list[NeedResponse])
def get_needs(
    # El nombre interno de Python es need_type, siguiendo las convenciones
    # en inglés. El alias mantiene "tipo" como nombre público de la API.
    #
    # Por ejemplo:
    # /api/necesidades?tipo=agua
    need_type: NeedType | None = Query(default=None, alias="tipo"),
    # Internamente utilizamos status_filter.
    # El alias mantiene "estado" en la URL que utiliza el frontend.
    #
    # Por ejemplo:
    # /api/necesidades?estado=abierta
    status_filter: NeedStatus | None = Query(default=None, alias="estado"),
):
    """Devuelve las necesidades con filtros opcionales.

    Los filtros públicos continúan en español:

    - Sin filtros, devuelve todas las necesidades.
    - Con tipo, devuelve solamente las de ese tipo.
    - Con estado, devuelve solamente las de ese estado.
    - Con ambos, devuelve las que cumplen las dos condiciones.
    """

    return list_needs(
        need_type=need_type,
        status=status_filter,
    )


@router.get(
    "/{need_id}",
    response_model=NeedResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Necesidad no encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Necesidad no encontrada",
                        "detalle": "No existe la necesidad con identificador 99999.",
                    }
                }
            },
        },
    },
)
def get_need_by_id(need_id: int):
    """Devuelve una única necesidad por su identificador.

    Se usa, por ejemplo, para abrir el detalle de un marcador del mapa
    sin tener que descargar de nuevo la lista completa.
    """

    need = get_need(need_id)

    if need is None:
        return _error_necesidad_no_encontrada(need_id)

    return need


@router.post(
    "",
    response_model=NeedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_need(need: NeedCreate):
    """Valida y registra una necesidad nueva.

    El formulario simplificado del frontend solo obliga a enviar:

    - tipo (una de las 8 categorías cerradas)
    - latitud / longitud

    titulo, descripcion y prioridad son opcionales: si no llegan,
    el servidor genera un título a partir de la categoría y usa
    prioridad "media" por defecto. id, estado y creado_en los genera
    siempre el servidor.
    """

    return create_need(need)


@router.patch(
    "/{need_id}",
    response_model=NeedResponse,
    responses={
        # Documentamos el error que se produce cuando el identificador
        # recibido no corresponde a ninguna necesidad.
        status.HTTP_404_NOT_FOUND: {
            "description": "Necesidad no encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Necesidad no encontrada",
                        "detalle": "No existe la necesidad con identificador 99999.",
                    }
                }
            },
        },
        # Documentamos el error que se produce al intentar saltar estados,
        # retroceder o reabrir una necesidad que ya estaba cubierta.
        status.HTTP_409_CONFLICT: {
            "description": "Transición de estado no válida",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Transición de estado no válida",
                        "detalle": (
                            "La necesidad no puede saltar estados, "
                            "retroceder ni reabrirse."
                        ),
                    }
                }
            },
        },
    },
)
def change_need_status(
    # FastAPI obtiene el identificador de la propia URL.
    need_id: int,
    # El frontend envía {"estado": "..."}.
    # NeedStatusUpdate utiliza el alias "estado", pero internamente
    # guarda el valor validado en el atributo inglés status.
    update: NeedStatusUpdate,
):
    """Cambia el estado de una necesidad existente.

    La única transición permitida es:

    - abierta → cubierta

    No se permite saltar estados (no existen estados intermedios),
    retroceder ni reabrir una necesidad que ya está cubierta.
    """

    try:
        updated_need = update_need_status(
            need_id=need_id,
            status=update.status,
        )

    except InvalidStatusTransition:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "Transición de estado no válida",
                "detalle": (
                    "La necesidad no puede saltar estados, " "retroceder ni reabrirse."
                ),
            },
        )

    if updated_need is None:
        return _error_necesidad_no_encontrada(need_id)

    return updated_need
