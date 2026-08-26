"""Esquemas de validación del módulo de personas.

Los nombres de Python siguen la convención técnica en inglés. Los alias en
español conservan el contrato JSON público utilizado por el frontend.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class PersonStatus(str, Enum):
    """Estados admitidos para una persona."""

    MISSING = "desaparecida"
    LOCATED = "localizada"
    SAFE = "estoy_bien"


class PersonBase(BaseModel):
    """Campos comunes para crear y representar una persona."""

    name: str | None = Field(default=None, alias="nombre")
    age: int | str | None = Field(default=None, alias="edad")
    status: PersonStatus | str | None = Field(default=None, alias="estado")
    last_location: str | None = Field(default=None, alias="ultima_ubicacion")
    reported_by: str | None = Field(default=None, alias="reportado_por")
    description: str | None = Field(default=None, alias="descripcion")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )


class PersonCreate(PersonBase):
    """Datos necesarios para crear una persona."""

    version: int = 1
    client_id: str | None = None
    updated_at: str | None = None
    is_deleted: int = 0
    created_at: datetime | str | None = Field(
        default=None,
        alias="creado_en",
    )

    model_config = ConfigDict(
        populate_by_name=True,
        by_alias=True,
        from_attributes=True,
        extra="ignore",
    )


class PersonResponse(PersonBase):
    """Representación completa de una persona devuelta por la API."""

    id: int

    version: int = 1
    client_id: str | None = None
    updated_at: str | None = None
    is_deleted: int = 0

    created_at: datetime | str | None = Field(
        default=None,
        alias="creado_en",
    )

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        extra="ignore",
    )


class PersonSafeRequest(BaseModel):
    """Entrada para marcar como segura una persona ya registrada."""

    model_config = ConfigDict(extra="forbid")

    person_id: int = Field(
        alias="id_persona",
        gt=0,
    )