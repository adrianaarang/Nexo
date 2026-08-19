"""Operaciones SQLite del módulo de necesidades.

La validación del contenido pertenece a ``schemas.py``. Este módulo se ocupa
solo de consultas parametrizadas y devuelve diccionarios fáciles de serializar.
"""
from sqlite3 import Row
from typing import Any

from db.database import get_cursor
from modules.necesidades.schemas import (
    EstadoNecesidad,
    NecesidadCrear,
    TipoNecesidad,
)


class TransicionEstadoInvalida(ValueError):
    """Permite que la capa de rutas traduzca un cambio inválido a HTTP 409."""


# Una necesidad solo puede avanzar; no se puede saltar un paso ni reabrirla.
TRANSICIONES_ESTADO = {
    EstadoNecesidad.ABIERTA: EstadoNecesidad.EN_PROCESO,
    EstadoNecesidad.EN_PROCESO: EstadoNecesidad.CUBIERTA,
}


def _fila_a_dict(fila: Row | None) -> dict[str, Any] | None:
    """Convierte una fila SQLite en un diccionario sin exponer el cursor."""

    return dict(fila) if fila is not None else None


def listar_necesidades(
    estado: EstadoNecesidad | None = None,
    tipo: TipoNecesidad | None = None,
) -> list[dict[str, Any]]:
    """Lee las necesidades, con filtros opcionales y un orden estable."""

    # Se construye únicamente la cláusula WHERE; los valores siempre se envían
    # como parámetros para evitar que la entrada del cliente se interprete
    # como parte de la consulta SQL.
    condiciones: list[str] = []
    parametros: list[str] = []

    if estado is not None:
        condiciones.append("estado = ?")
        parametros.append(estado.value)
    if tipo is not None:
        condiciones.append("tipo = ?")
        parametros.append(tipo.value)

    consulta = "SELECT * FROM necesidades"
    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)
    consulta += " ORDER BY id ASC"

    with get_cursor() as cursor:
        # ORDER BY id mantiene un resultado predecible para API, mapa y tests.
        cursor.execute(consulta, parametros)
        return [dict(fila) for fila in cursor.fetchall()]


def obtener_necesidad(necesidad_id: int) -> dict[str, Any] | None:
    """Lee una necesidad por su identificador o devuelve ``None``."""

    with get_cursor() as cursor:
        # Devolver None deja que routes.py decida la respuesta HTTP apropiada.
        cursor.execute(
            "SELECT * FROM necesidades WHERE id = ?",
            (necesidad_id,),
        )
        return _fila_a_dict(cursor.fetchone())


def crear_necesidad(necesidad: NecesidadCrear) -> dict[str, Any]:
    """Guarda una necesidad validada y devuelve el registro creado."""

    with get_cursor() as cursor:
        # El esquema ya validó los campos; aquí solo se persisten con una
        # consulta parametrizada. SQLite asigna id, estado y fecha de creación.
        cursor.execute(
            """INSERT INTO necesidades
               (titulo, tipo, descripcion, latitud, longitud, prioridad)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                necesidad.titulo,
                necesidad.tipo.value,
                necesidad.descripcion,
                necesidad.latitud,
                necesidad.longitud,
                necesidad.prioridad.value,
            ),
        )
        necesidad_id = cursor.lastrowid
        # Se devuelve la fila completa para incluir los valores generados por
        # SQLite en la respuesta del endpoint POST.
        cursor.execute(
            "SELECT * FROM necesidades WHERE id = ?",
            (necesidad_id,),
        )
        # La fila existe porque la inserción y la lectura usan la misma conexión.
        return dict(cursor.fetchone())


def actualizar_estado_necesidad(
    necesidad_id: int,
    estado: EstadoNecesidad,
) -> dict[str, Any] | None:
    """Avanza el estado sin permitir saltos ni reabrir una necesidad.

    Repetir el estado actual es válido para que los reintentos del cliente sean
    idempotentes. Un identificador inexistente se comunica mediante ``None``.
    """

    with get_cursor() as cursor:
        # Es necesario leer primero para distinguir un id inexistente de una
        # transición que no respeta el flujo del negocio.
        cursor.execute(
            "SELECT * FROM necesidades WHERE id = ?",
            (necesidad_id,),
        )
        fila_actual = cursor.fetchone()
        if fila_actual is None:
            return None

        estado_actual = EstadoNecesidad(fila_actual["estado"])
        # Aceptar el mismo estado hace seguro repetir una petición PATCH si la
        # conexión se corta antes de recibir la respuesta.
        if estado == estado_actual:
            return dict(fila_actual)

        if TRANSICIONES_ESTADO.get(estado_actual) != estado:
            raise TransicionEstadoInvalida(
                f"No se puede cambiar de {estado_actual.value} a {estado.value}"
            )

        # Solo se ejecuta el UPDATE después de validar la transición.
        cursor.execute(
            "UPDATE necesidades SET estado = ? WHERE id = ?",
            (estado.value, necesidad_id),
        )

        # La capa superior recibe siempre el registro tal como quedó guardado.
        cursor.execute(
            "SELECT * FROM necesidades WHERE id = ?",
            (necesidad_id,),
        )
        return _fila_a_dict(cursor.fetchone())
