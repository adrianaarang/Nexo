"""Pydantic schemas for the alerts API module.

Defines enum domain constraints, response data models, and validation contracts.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field


class SeverityEnum(str, Enum):
    """Enumeration of valid alert severity levels."""

    RED = "red"
    ORANGE = "orange"
    GREEN = "green"


class EventTypeEnum(str, Enum):
    """Enumeration of standardized disaster event classifications."""

    TERREMOTO = "terremoto"
    CICLON = "ciclon"
    INUNDACION = "inundacion"
    INCENDIO = "incendio"
    VOLCAN = "volcan"
    SEQUIA = "sequia"
    OTRO = "otro"


class RiskLevel(str, Enum):
    """Nivel de riesgo asignado por el gestor a una alerta de crisis."""

    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"


class AlertStatus(str, Enum):
    """Estado de una alerta del gestor según el contrato que consume el mapa."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    ALTO_RIESGO = "alto_riesgo"


class AlertCreate(BaseModel):
    """Cuerpo de la petición para crear una alerta del gestor."""

    nivel_riesgo: RiskLevel = Field(
        ...,
        description="Nivel de riesgo de la alerta (bajo, medio, alto).",
    )
    zona: Dict[str, Any] = Field(
        ...,
        description="Zona afectada en GeoJSON Polygon (objeto).",
    )
    gestor_token: str = Field(
        ...,
        min_length=1,
        description="Token del gestor que crea la alerta (MVP sin login).",
    )
    titulo: str = Field(default="", max_length=300)
    descripcion: str = Field(default="", max_length=2000)
    tipo: Optional[EventTypeEnum] = Field(
        default=None,
        description="Tipo de evento opcional, reusa EventTypeEnum.",
    )


class AlertUpdate(BaseModel):
    """Cuerpo de la petición para actualizar una alerta del gestor.

    Todos los campos son opcionales; solo se modifican los presentes.
    """

    nivel_riesgo: Optional[RiskLevel] = None
    zona: Optional[Dict[str, Any]] = None
    titulo: Optional[str] = Field(default=None, max_length=300)
    descripcion: Optional[str] = Field(default=None, max_length=2000)
    tipo: Optional[EventTypeEnum] = None
    activa: Optional[bool] = None


class AlertResponse(BaseModel):
    """Data model representing a single alert item in API responses.

    Unifica alertas externas (GDACS / Protección Civil) y alertas del gestor.
    Los campos de gestor y los del contrato del mapa (risk_level, status, zone)
    son opcionales porque las alertas externas no los tienen.
    """

    model_config = ConfigDict(from_attributes=True)

    id: Any = Field(
        ...,
        description="Identificador de la alerta (str para GDACS, int para gestor).",
    )
    fuente: Optional[str] = Field(
        default=None,
        description="Origen de la alerta (gdacs, proteccion_civil, gestor).",
    )
    tipo: Optional[EventTypeEnum] = Field(
        default=None,
        description="Clasificación del evento (puede faltar en alertas del gestor).",
    )
    titulo: Optional[str] = Field(default=None)
    descripcion: Optional[str] = Field(default=None)
    severidad: Optional[SeverityEnum] = Field(
        default=None,
        description="Severidad de la fuente externa (no aplica a gestor).",
    )
    pais: Optional[str] = Field(default=None)
    lat: Optional[float] = Field(default=None)
    lon: Optional[float] = Field(default=None)
    fecha: Optional[datetime] = Field(default=None)
    enlace: Optional[str] = Field(default=None)

    # Campos propios de las alertas del gestor
    nivel_riesgo: Optional[RiskLevel] = Field(default=None)
    zona: Optional[Dict[str, Any]] = Field(default=None)
    activa: Optional[bool] = Field(default=None)
    gestor_token: Optional[str] = Field(
        default=None,
        description="Solo se expone en respuestas de creación/consulta individual.",
    )

    # Contrato que consume el mapa (Equipo 4)
    risk_level: Optional[str] = Field(
        default=None,
        description="Nivel de riesgo normalizado para el mapa.",
    )
    status: Optional[str] = Field(
        default=None,
        description="Estado para el mapa: inactive, active, alto_riesgo.",
    )
    zone: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Zona GeoJSON que consume el mapa.",
    )
