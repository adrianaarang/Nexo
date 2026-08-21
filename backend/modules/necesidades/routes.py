"""Endpoints del módulo de necesidades.

Este archivo se encarga de recibir las peticiones HTTP relacionadas
con las necesidades del mapa y devolver una respuesta al frontend.

Aquí no escribimos directamente las consultas SQL. Para acceder a la
base de datos utilizamos las funciones preparadas en models.py.
"""

# Importamos las herramientas necesarias de FastAPI:
#
# - APIRouter: agrupa los endpoints relacionados con necesidades.
# - HTTPException: permite devolver errores HTTP al frontend.
# - status: contiene nombres descriptivos para los códigos HTTP.
from fastapi import APIRouter, HTTPException, status

# Importamos las funciones y errores de models.py que necesitamos:
#
# - TransicionEstadoInvalida: avisa cuando se intenta realizar
#   un cambio de estado que no está permitido.
# - actualizar_estado_necesidad: cambia el estado en la base de datos.
# - crear_necesidad: guarda una necesidad nueva.
# - listar_necesidades: consulta las necesidades guardadas.
from modules.necesidades.models import (
    TransicionEstadoInvalida,
    actualizar_estado_necesidad,
    crear_necesidad,
    listar_necesidades,
)

# Importamos los schemas y enumeraciones necesarios:
#
# - EstadoNecesidad: contiene los estados permitidos.
# - NecesidadActualizarEstado: valida el nuevo estado enviado en el PATCH.
# - NecesidadCrear: valida los datos recibidos al crear una necesidad.
# - NecesidadRespuesta: valida la información devuelta por la API.
# - TipoNecesidad: contiene los tipos de necesidad permitidos.
from modules.necesidades.schemas import (
    EstadoNecesidad,
    NecesidadActualizarEstado,
    NecesidadCrear,
    NecesidadRespuesta,
    TipoNecesidad,
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
# Cada elemento deberá cumplir la estructura de NecesidadRespuesta.
@router.get("", response_model=list[NecesidadRespuesta])
def obtener_necesidades(
    # Filtro opcional por tipo.
    # Puede recibir valores como agua, alimento, medicina o refugio.
    # Si no se envía, su valor será None y no se filtrará por tipo.
    tipo: TipoNecesidad | None = None,

    # Filtro opcional por estado.
    # Puede recibir abierta, en_proceso o cubierta.
    # Si no se envía, su valor será None y no se filtrará por estado.
    estado: EstadoNecesidad | None = None,
):
    """Devuelve las necesidades guardadas en la base de datos.

    Los filtros de tipo y estado son opcionales:

    - Sin filtros, devuelve todas las necesidades.
    - Con tipo, devuelve solamente las de ese tipo.
    - Con estado, devuelve solamente las de ese estado.
    - Con ambos, devuelve las que cumplan las dos condiciones.
    """

    # Llamamos a la función de models.py que realiza la consulta SQL.
    # Le entregamos los filtros recibidos en la URL.
    #
    # Ejemplos:
    # /api/necesidades
    # /api/necesidades?tipo=agua
    # /api/necesidades?estado=abierta
    # /api/necesidades?tipo=agua&estado=abierta
    necesidades = listar_necesidades(
        tipo=tipo,
        estado=estado,
    )

    # Devolvemos el resultado a FastAPI.
    # FastAPI comprobará que cada elemento cumple NecesidadRespuesta
    # y lo convertirá automáticamente en JSON para el frontend.
    return necesidades


# Este decorador convierte la función situada debajo en un endpoint POST.
#
# La dirección vuelve a estar vacía ("") porque se añade al prefijo:
# /api/necesidades + "" = /api/necesidades
#
# POST se utiliza cuando el cliente quiere crear un recurso nuevo.
#
# response_model indica que devolveremos una necesidad completa,
# incluyendo el id, el estado inicial y la fecha de creación.
#
# status_code indica el código HTTP que se devolverá si todo funciona.
# 201 Created significa que el recurso se ha creado correctamente.
@router.post(
    "",
    response_model=NecesidadRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_necesidad(necesidad: NecesidadCrear):
    """Valida y registra una necesidad nueva.

    El frontend debe enviar:

    - titulo
    - tipo
    - descripcion
    - latitud
    - longitud
    - prioridad, que es opcional

    El frontend no debe enviar id, estado ni creado_en porque esos
    campos los genera automáticamente el servidor.
    """

    # Cuando FastAPI recibe el JSON, utiliza NecesidadCrear para comprobar:
    #
    # - que estén presentes los campos obligatorios;
    # - que el tipo y la prioridad sean válidos;
    # - que las coordenadas estén dentro de los rangos permitidos;
    # - que el título y la descripción tengan una longitud válida.
    #
    # Si algún dato es incorrecto, FastAPI devuelve un error 422
    # antes de ejecutar el código situado debajo.

    # Enviamos los datos ya validados a la función de models.py.
    # Esa función realiza el INSERT en SQLite y recupera el registro
    # completo después de crearlo.
    necesidad_creada = crear_necesidad(necesidad)

    # Devolvemos la necesidad completa.
    # FastAPI la valida con NecesidadRespuesta y la convierte en JSON.
    return necesidad_creada


# Este endpoint permite cambiar el estado de una necesidad existente.
#
# PATCH se utiliza para modificar solamente una parte de un recurso.
# En este caso, no cambiamos el título, el tipo o la ubicación:
# modificamos únicamente el estado.
#
# {necesidad_id} es una parte variable de la dirección.
# Por ejemplo:
# /api/necesidades/5/estado
#
# response_model indica que devolveremos la necesidad completa
# después de actualizarla.
@router.patch(
    "/{necesidad_id}/estado",
    response_model=NecesidadRespuesta,
)
def cambiar_estado_necesidad(
    # FastAPI obtiene este número directamente de la URL.
    necesidad_id: int,

    # FastAPI obtiene el nuevo estado del JSON enviado por el frontend
    # y lo valida utilizando NecesidadActualizarEstado.
    actualizacion: NecesidadActualizarEstado,
):
    """Cambia el estado de una necesidad existente.

    Los cambios permitidos son:

    - abierta → en_proceso
    - en_proceso → cubierta

    No se permite saltar estados, retroceder ni reabrir
    una necesidad que ya está cubierta.
    """

    try:
        # Intentamos actualizar el estado mediante la función de models.py.
        #
        # actualizacion.estado contiene el nuevo estado enviado
        # por el frontend, por ejemplo EstadoNecesidad.EN_PROCESO.
        necesidad_actualizada = actualizar_estado_necesidad(
            necesidad_id=necesidad_id,
            estado=actualizacion.estado,
        )

    except TransicionEstadoInvalida as error:
        # Si models.py detecta un cambio no permitido, convertimos
        # ese error de Python en una respuesta HTTP 409 Conflict.
        #
        # Por ejemplo, intentar pasar directamente:
        # abierta → cubierta
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    # models.py devuelve None cuando no encuentra una necesidad
    # con el identificador recibido.
    if necesidad_actualizada is None:
        # Convertimos esa ausencia en un error HTTP 404 Not Found.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha encontrado la necesidad indicada.",
        )

    # Si la necesidad existe y la transición es válida,
    # devolvemos el registro completo después de actualizarlo.
    return necesidad_actualizada
