"""Esquemas de validación del módulo de necesidades.

Los nombres de Python siguen la convención técnica en inglés. Los alias en
español conservan el contrato JSON ya compartido con el equipo de frontend.

REDISEÑO (rehecho tras el sprint anterior): categorías cerradas a 8 iconos
(ver NEED_TYPE_LABELS) y ciclo de vida simplificado a abierta -> cubierta,
tal y como se acordó en docs/reparto-trabajo.md para el Equipo 1.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class NeedType(str, Enum):
    """Categorías cerradas de necesidad admitidas por el formulario y el mapa."""

    # FastAPI serializa estos enums con los valores acordados del contrato JSON.
    WATER = "agua"
    FOOD = "alimentos"
    PHARMACY = "parafarmacia"
    CLOTHING = "ropa"
    HYGIENE = "higiene"
    SHELTER = "refugio"
    TRANSPORT = "transporte"
    OTHER = "otros"


# Etiqueta con emoji para cada categoría, tal y como se van a mostrar en el
# formulario simplificado y en las tarjetas del mapa. Vive aquí (y no solo
# en el frontend) para que la respuesta de la API ya incluya el texto listo
# para pintar (ver NeedResponse.category_label) y frontend no duplique el mapeo.
NEED_TYPE_LABELS: dict[NeedType, str] = {
    NeedType.WATER: "💧 Agua",
    NeedType.FOOD: "🍞 Alimentos",
    NeedType.PHARMACY: "💊 Parafarmacia",
    NeedType.CLOTHING: "👕 Ropa",
    NeedType.HYGIENE: "🧴 Higiene",
    NeedType.SHELTER: "🏠 Refugio",
    NeedType.TRANSPORT: "🚗 Transporte",
    NeedType.OTHER: "📦 Otros",
}


class NeedPriority(str, Enum):
    """Prioridad declarada al registrar una necesidad."""

    LOW = "baja"
    MEDIUM = "media"
    HIGH = "alta"
    CRITICAL = "critica"


class NeedStatus(str, Enum):
    """Estados disponibles durante el ciclo de vida de una necesidad.

    Simplificado a dos pasos (abierta -> cubierta): el estado intermedio
    "en_proceso" del sprint anterior se elimina para volver al alcance
    acordado en docs/reparto-trabajo.md.
    """

    OPEN = "abierta"
    COVERED = "cubierta"


class NeedBase(BaseModel):
    """Campos que describen, ubican y priorizan una necesidad."""

    # Se rechazan claves desconocidas para detectar pronto errores de integración.
    # Los alias obligan a que la API reciba exactamente las claves del contrato.
    model_config = ConfigDict(extra="forbid")

    # El formulario simplificado no obliga a escribir un título: si llega
    # vacío, el servicio (services.py) genera uno a partir de la categoría.
    title: str = Field(default="", alias="titulo", max_length=120)
    need_type: NeedType = Field(alias="tipo")
    # La descripción también pasa a ser opcional para que registrar una
    # necesidad sea lo más rápido posible: categoría + ubicación bastan.
    description: str = Field(default="", alias="descripcion", max_length=1000)
    # Texto legible del lugar (p. ej. "Calle Mayor 3, Valencia"). Lo rellena
    # el frontend al geocodificar la dirección escrita, o al hacer
    # geocodificación inversa tras usar el GPS o un clic en el mapa (ver
    # geocodificacion.js). Se guarda tal cual para poder mostrarlo en la
    # tarjeta y el popup sin depender solo de las coordenadas.
    #
    # Nominatim (el servicio de geocodificación) puede devolver direcciones
    # muy largas (barrio, comarca, código postal, país...), así que en vez
    # de rechazarlas se recortan a este límite en strip_text_fields de abajo;
    # max_length coincide con ese recorte para que nunca pueda saltar.
    address: str = Field(default="", alias="direccion", max_length=300)
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

    @field_validator("title", "description", "address", mode="before")
    @classmethod
    def strip_text_fields(cls, value: object, info) -> object:
        """Elimina espacios laterales y, para "address", recorta si hace falta."""

        if not isinstance(value, str):
            return value

        value = value.strip()
        if info.field_name == "address":
            value = value[:300]
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
    # Campo calculado (no vive en la base de datos): etiqueta con emoji
    # lista para pintar en la tarjeta o el popup del mapa, sin que el
    # frontend tenga que mantener su propia copia de NEED_TYPE_LABELS.
    category_label: str = Field(default="", alias="categoria_etiqueta")

    @model_validator(mode="after")
    def _fill_category_label(self) -> "NeedResponse":
        if not self.category_label:
            object.__setattr__(
                self, "category_label", NEED_TYPE_LABELS[self.need_type]
            )
        return self
