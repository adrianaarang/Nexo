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
    """Esquema base con mapeo entre nombres en inglés y alias en español."""
    name: str | None = Field(default=None, alias="nombre")
    age: int | str | None = Field(default=None, alias="edad")
    status: PersonStatus | str | None = Field(default=None, alias="estado")
    last_location: str | None = Field(default=None, alias="ultima_ubicacion")
    reported_by: str | None = Field(default=None, alias="reportado_por")
    description: str | None = Field(default=None, alias="descripcion")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )

class PersonCreate(PersonBase):
    """Representación completa de una persona devuelta por la API."""
    id: int
    version: int = 1
    client_id: str | None = None
    updated_at: str | None = None
    is_deleted: int = 0
    created_at: datetime | str | None = Field(default=None, alias="creado_en")

    model_config = ConfigDict(
        populate_by_name=True,
        by_alias=True,  # Importante: exporta con alias en español por defecto
        from_attributes=True,
        extra="ignore",
    )

class PersonResponse(BaseModel):
    """Representación completa de una persona devuelta por la API."""
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        from_attributes=True,
    )

    id: int
    nombre: str | None = Field(default=None, alias="name")
    edad: int | str | None = Field(default=None, alias="age")
    estado: PersonStatus | str | None = Field(default=None, alias="status")
    ultima_ubicacion: str | None = Field(default=None, alias="last_location")
    reportado_por: str | None = Field(default=None, alias="reported_by")
    descripcion: str | None = Field(default=None, alias="description")
    created_at: datetime | str | None = Field(default=None, alias="creado_en")
    version: int = 1
    client_id: str | None = None
    updated_at: str | None = None
    is_deleted: int = 0

class PersonSafeRequest(BaseModel):
    """Entrada para marcar como segura una persona ya registrada."""
    model_config = ConfigDict(extra="forbid")
    person_id: int = Field(alias="id_persona", gt=0)