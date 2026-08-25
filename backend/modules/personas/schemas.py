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
    """Esquema base con las prioridades comunes de  una persona."""
    name: str = Field(alias = "nombre")
    age: int | None = Field(None, alias = "edad")
    lat_location: str | None = Field(None, alias = "ultima_ubicacion")
    description: str | None = Field(None, alias = "descripcion")
    status: PersonStatus = Field(PersonStatus.MISSING, alias = "estado")
    reported_by: str | None = Field(None, alias = "reportado_por")

class PersonCreate(PersonBase):
    """Esquema utilizado para la creación de un nuevo registro"""
    client_id: str | None = None

class PersonResponse(BaseModel):
    """Representación completa de una persona devuelta por la API."""
    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    created_at: datetime = Field(alias="creado_en")
    version: int = 1
    client_id: str | None = None
    updated_at: str | None = None
    is_deleted: int = 0

class PersonSafeRequest(BaseModel):
    """Entrada para marcar como segura una persona ya registrada."""
    model_config = ConfigDict(extra="forbid")
    person_id: int = Field(alias="id_persona", gt=0)