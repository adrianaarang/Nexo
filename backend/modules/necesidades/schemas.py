"""Esquemas de validación del módulo de necesidades.

Los valores permitidos coinciden con el esquema SQLite inicial. Mantenerlos
centralizados evita que la API y la base de datos acepten contratos distintos.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TipoNecesidad(str, Enum):
    """Categorías que puede representar el mapa en el MVP."""

    # Al heredar de str, FastAPI serializa cada miembro con el valor JSON
    # acordado con las personas responsables del frontend.
    AGUA = "agua"
    ALIMENTO = "alimento"
    MEDICINA = "medicina"
    REFUGIO = "refugio"
    HERRAMIENTAS = "herramientas"
    TRANSPORTE = "transporte"


class PrioridadNecesidad(str, Enum):
    """Prioridad declarada al registrar una necesidad."""

    # La prioridad crítica se conserva como "critica" sin tilde en la API.
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"
    CRITICA = "critica"


class EstadoNecesidad(str, Enum):
    """Estados disponibles durante el seguimiento de una necesidad."""

    # Los valores reflejan literalmente el contrato JSON compartido.
    ABIERTA = "abierta"
    EN_PROCESO = "en_proceso"
    CUBIERTA = "cubierta"


class NecesidadBase(BaseModel):
    """Campos comunes que describen y ubican una necesidad."""

    # Rechazar claves desconocidas ayuda a detectar errores del cliente pronto.
    model_config = ConfigDict(extra="forbid")

    # Título y descripción se limitan para evitar textos vacíos o cargas
    # desproporcionadas en las tarjetas y popups del mapa.
    titulo: str = Field(min_length=3, max_length=120)
    tipo: TipoNecesidad
    descripcion: str = Field(min_length=3, max_length=1000)
    # Las coordenadas deben ser finitas y pertenecer a los rangos geográficos.
    latitud: float = Field(ge=-90, le=90, allow_inf_nan=False)
    longitud: float = Field(ge=-180, le=180, allow_inf_nan=False)
    # Si el usuario no selecciona prioridad, el contrato aplica "media".
    prioridad: PrioridadNecesidad = PrioridadNecesidad.MEDIA

    @field_validator("titulo", "descripcion", mode="before")
    @classmethod
    def normalizar_texto(cls, texto: object) -> object:
        """Elimina espacios accidentales antes de comprobar la longitud."""

        if isinstance(texto, str):
            return texto.strip()
        return texto


class NecesidadCrear(NecesidadBase):
    """Datos admitidos al crear; id, estado y fecha los genera el servidor."""


class NecesidadActualizarEstado(BaseModel):
    """Único cambio permitido por el endpoint de estado del MVP."""

    model_config = ConfigDict(extra="forbid")

    # No se aceptan otros campos para impedir modificaciones accidentales.
    estado: EstadoNecesidad


class NecesidadRespuesta(NecesidadBase):
    """Representación completa que se devuelve al cliente."""

    # Estos campos los controla la persistencia, nunca el formulario de alta.
    id: int = Field(gt=0)
    estado: EstadoNecesidad
    creado_en: datetime
