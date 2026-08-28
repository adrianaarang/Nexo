"""Endpoints del módulo de necesidades.

Este archivo se encarga de recibir las peticiones HTTP relacionadas
con las necesidades del mapa y devolver una respuesta al frontend.

Aquí no escribimos directamente las consultas SQL. Para acceder a la
base de datos utilizamos las funciones preparadas en models.py.
"""

# Importamos las herramientas necesarias de FastAPI:
#
# - APIRouter: agrupa los endpoints relacionados con necesidades.
# - Query: permite usar nombres internos en inglés manteniendo los
#   parámetros públicos de la API en español.
# - status: contiene nombres descriptivos para los códigos HTTP.
# - JSONResponse: permite devolver los errores con el formato único
#   acordado en las convenciones: {"error", "detalle"}.
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

# Importamos las funciones y errores de models.py que necesitamos:
#
# - InvalidStatusTransition: avisa cuando se intenta realizar
#   un cambio de estado que no está permitido.
# - create_need: guarda una necesidad nueva.
# - list_needs: consulta las necesidades guardadas.
# - update_need_status: cambia el estado de una necesidad.
#
# Los nombres internos están en inglés para seguir las convenciones
# técnicas del proyecto.
from modules.necesidades.models import InvalidStatusTransition
from modules.necesidades.services import (
    create_need,
    list_needs,
    update_need_status,
)

# Importamos los schemas y enumeraciones necesarios:
#
# - NeedCreate: valida los datos recibidos al crear una necesidad.
# - NeedResponse: valida la información devuelta por la API.
# - NeedStatus: contiene los estados permitidos.
# - NeedStatusUpdate: valida el nuevo estado enviado en el PATCH.
# - NeedType: contiene los tipos de necesidad permitidos.
#
# Los nombres internos son ingleses, pero los alias definidos en
# schemas.py mantienen el contrato JSON público en español.
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


# Este decorador convierte la función situada debajo en un endpoint GET.
#
# La ruta está vacía ("") porque se añade al prefijo del router:
# /api/necesidades + "" = /api/necesidades
#
# response_model indica que la respuesta será una lista de necesidades.
# Cada elemento se validará mediante NeedResponse.
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

    # Llamamos a la función de models.py utilizando sus nuevos
    # parámetros internos en inglés.
    needs = list_needs(
        need_type=need_type,
        status=status_filter,
    )

    # NeedResponse utiliza alias para convertir los nombres internos
    # al contrato JSON público en español.
    return needs


# Este decorador convierte la función situada debajo en un endpoint POST.
#
# POST se utiliza para crear un recurso nuevo.
#
# response_model indica que la respuesta será una necesidad completa
# validada mediante NeedResponse.
#
# status_code=201 indica que el recurso se ha creado correctamente.
@router.post(
    "",
    response_model=NeedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_need(need: NeedCreate):
    """Valida y registra una necesidad nueva.

    El frontend continúa enviando los campos públicos en español:

    - titulo
    - tipo
    - descripcion
    - latitud
    - longitud
    - prioridad, que es opcional

    El frontend no envía id, estado ni creado_en porque estos campos
    los genera automáticamente el servidor.
    """

    # FastAPI recibe el JSON público en español.
    #
    # NeedCreate utiliza los alias definidos en schemas.py para
    # transformar esos campos en atributos internos en inglés:
    #
    # titulo      → title
    # tipo        → need_type
    # descripcion → description
    # latitud     → latitude
    # longitud    → longitude
    # prioridad   → priority
    #
    # También valida que los campos y sus valores sean correctos.

    # Enviamos la necesidad validada a la función de models.py.
    # create_need realiza el INSERT en SQLite y devuelve el registro
    # completo con id, estado inicial y fecha de creación.
    created_need = create_need(need)

    # NeedResponse valida el resultado y utiliza los alias para devolver
    # nuevamente el contrato JSON público en español.
    return created_need


# Este endpoint permite cambiar únicamente el estado de una necesidad.
#
# PATCH se utiliza cuando queremos modificar una parte concreta de
# un recurso existente, sin sustituir todos sus datos.
#
# {need_id} es la parte variable de la URL.
# Por ejemplo:
# /api/necesidades/5/estado
#
# response_model indica que una actualización correcta devolverá
# la necesidad completa, validada mediante NeedResponse.
#
# responses documenta en Swagger los posibles errores del endpoint.
# No crea esos errores ni cambia su funcionamiento; solamente explica
# qué códigos y qué JSON puede recibir el frontend.
@router.patch(
    "/{need_id}/estado",
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
                        "detalle": (
                            "No existe una necesidad con el " "identificador 99999."
                        ),
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

    La transición permitida es abierta → cubierta. Repetir el estado
    actual es idempotente; no se permite reabrir una necesidad cubierta.
    """

    try:
        # Intentamos actualizar la necesidad mediante models.py.
        #
        # update.status contiene el nuevo estado después de haber sido
        # validado por NeedStatusUpdate.
        updated_need = update_need_status(
            need_id=need_id,
            status=update.status,
        )

    except InvalidStatusTransition:
        # Si se intenta realizar una transición no permitida,
        # devolvemos HTTP 409 Conflict.
        #
        # JSONResponse nos permite respetar el formato único de errores
        # acordado en las convenciones del proyecto.
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "Transición de estado no válida",
                "detalle": (
                    "La necesidad no puede saltar estados, " "retroceder ni reabrirse."
                ),
            },
        )

    # models.py devuelve None cuando no encuentra una necesidad
    # con el identificador recibido.
    if updated_need is None:
        # Convertimos la ausencia en HTTP 404 Not Found y mantenemos
        # el formato común {"error", "detalle"}.
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Necesidad no encontrada",
                "detalle": (f"No existe una necesidad con el identificador {need_id}."),
            },
        )

    # Si la necesidad existe y la transición es válida,
    # devolvemos el registro completo actualizado.
    return updated_need
