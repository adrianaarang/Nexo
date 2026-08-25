"""Validación de entrada/salida de voluntarios.

Los nombres de Python siguen la convención técnica en inglés. Los alias en
español conservan el contrato JSON ya compartido con el equipo de frontend.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class VolunteerStatus(str, Enum):
    """Estados del ciclo de validación de un voluntario."""

    PENDING = "pendiente"
    APPROVED = "aprobado"
    REJECTED = "rechazado"


class VolunteerBase(BaseModel):
    """Campos que describen a un voluntario y su disponibilidad horaria."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(alias="nombre", min_length=2, max_length=120)
    contact: str = Field(alias="contacto", min_length=3, max_length=200)
    skills: str = Field(alias="habilidades", min_length=2, max_length=500)
    availability: str = Field(
        default="inmediata",
        alias="disponibilidad",
        max_length=100,
    )

    @field_validator("name", "contact", "skills", "availability", mode="before")
    @classmethod
    def strip_text_fields(cls, value: object) -> object:
        """Elimina espacios laterales antes de validar la longitud."""

        if isinstance(value, str):
            return value.strip()
        return value


class VolunteerCreate(VolunteerBase):
    """Entrada de creación; el servidor controla id, estado y fecha."""


class VolunteerDocumentResponse(BaseModel):
    """Metadatos de un documento adjunto (sin ruta interna del servidor)."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    original_name: str = Field(alias="nombre_original")
    mime_type: str = Field(alias="tipo_mime")
    created_at: datetime = Field(alias="creado_en")


class VolunteerResponse(VolunteerBase):
    """Representación pública de un voluntario aprobado."""

    id: int = Field(gt=0)
    status: VolunteerStatus = Field(alias="estado")
    is_available: bool = Field(alias="disponible")
    created_at: datetime = Field(alias="creado_en")


class VolunteerRegistrationResponse(VolunteerBase):
    """Respuesta del registro antes de la validación administrativa."""

    id: int = Field(gt=0)
    status: VolunteerStatus = Field(alias="estado")
    is_available: bool = Field(alias="disponible")
    documents: list[VolunteerDocumentResponse] = Field(
        default_factory=list,
        alias="documentos",
    )
    created_at: datetime = Field(alias="creado_en")


class VolunteerPendingResponse(VolunteerBase):
    """Vista administrativa de una solicitud pendiente."""

    id: int = Field(gt=0)
    status: VolunteerStatus = Field(alias="estado")
    is_available: bool = Field(alias="disponible")
    documents: list[VolunteerDocumentResponse] = Field(
        default_factory=list,
        alias="documentos",
    )
    created_at: datetime = Field(alias="creado_en")


class VolunteerAvailabilityUpdate(BaseModel):
    """Entrada para cambiar la disponibilidad activa del voluntario."""

    model_config = ConfigDict(extra="forbid")

    is_available: bool = Field(alias="disponible")


class VolunteerActionResponse(BaseModel):
    """Respuesta breve tras aprobar o rechazar una solicitud."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    status: VolunteerStatus = Field(alias="estado")
    message: str = Field(alias="mensaje")
