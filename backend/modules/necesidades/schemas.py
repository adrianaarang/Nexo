"""Esquemas de validación del módulo de necesidades.

Los nombres de Python siguen la convención técnica en inglés. Los alias en
español conservan el contrato JSON ya compartido con el equipo de frontend.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NeedType(str, Enum):
    """Categorías de necesidad admitidas por el mapa del MVP."""

    # FastAPI serializa estos enums con los valores acordados del contrato JSON.
    WATER = "agua"
    FOOD = "alimento"
    MEDICINE = "medicina"
    SHELTER = "refugio"
    TOOLS = "herramientas"
    TRANSPORT = "transporte"


class NeedPriority(str, Enum):
    """Prioridad declarada al registrar una necesidad."""

    LOW = "baja"
    MEDIUM = "media"
    HIGH = "alta"
    CRITICAL = "critica"


class NeedStatus(str, Enum):
    """Estados disponibles durante el ciclo de vida de una necesidad."""

    OPEN = "abierta"
    IN_PROGRESS = "en_proceso"
    COVERED = "cubierta"


class NeedBase(BaseModel):
    """Campos que describen, ubican y priorizan una necesidad."""

    # Se rechazan claves desconocidas para detectar pronto errores de integración.
    # Los alias obligan a que la API reciba exactamente las claves del contrato.
    model_config = ConfigDict(extra="forbid")

    title: str = Field(alias="titulo", min_length=3, max_length=120)
    need_type: NeedType = Field(alias="tipo")
    description: str = Field(alias="descripcion", min_length=3, max_length=1000)
    latitude: float = Field(alias="latitud", ge=-90, le=90, allow_inf_nan=False)
    longitude: float = Field(
        alias="longitud",
        ge=-180,
        le=180,
        allow_inf_nan=False,
    )
    priority: NeedPriority = Field(
        default=NeedPriority.MEDIUM,
        alias="prioridad",
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_text_fields(cls, value: object) -> object:
        """Elimina espacios laterales antes de validar la longitud."""

        if isinstance(value, str):
            return value.strip()
        return value


class NeedCreate(NeedBase):
    """Entrada de creación; el servidor controla id, estado y fecha."""


class NeedStatusUpdate(BaseModel):
    """Entrada admitida por el endpoint de actualización de estado."""

    model_config = ConfigDict(extra="forbid")

    # Una actualización de estado no admite ningún otro campo.
    status: NeedStatus = Field(alias="estado")


class NeedResponse(NeedBase):
    """Representación completa devuelta a los clientes de la API."""

    # Estos campos los genera la persistencia, nunca el formulario.
    id: int = Field(gt=0)
    status: NeedStatus = Field(alias="estado")
    created_at: datetime = Field(alias="creado_en")
