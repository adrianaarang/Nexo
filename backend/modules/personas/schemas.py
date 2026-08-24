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


class PersonSafeRequest(BaseModel):
    """Entrada para marcar como segura una persona ya registrada."""

    model_config = ConfigDict(extra="forbid")

    person_id: int = Field(alias="id_persona", gt=0)


class PersonResponse(BaseModel):
    """Representación completa de una persona devuelta por la API."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    name: str = Field(alias="nombre")
    status: PersonStatus = Field(alias="estado")
    last_location: str = Field(alias="ultima_ubicacion")
    reported_by: str = Field(alias="reportado_por")
    created_at: datetime = Field(alias="creado_en")
