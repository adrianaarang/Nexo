"""Pydantic schemas for the alerts API module.

Defines enum domain constraints, response data models, and validation contracts.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
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


class AlertResponse(BaseModel):
    """Data model representing a single alert item in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(
        ...,
        description="Unique alert identifier (e.g., gdacs-EQ2026xxxxx)",
    )
    fuente: str = Field(
        default="gdacs",
        description="Data source provider name",
    )
    tipo: EventTypeEnum = Field(
        ...,
        description="Standardized event type classification",
    )
    titulo: str = Field(
        default="",
        description="Short descriptive title of the alert",
    )
    descripcion: str = Field(
        default="",
        description="Detailed alert summary or description",
    )
    severidad: SeverityEnum = Field(
        ...,
        description="Severity level attribute",
    )
    pais: Optional[str] = Field(
        default="",
        description="Name of the affected country",
    )
    lat: Optional[float] = Field(
        default=None,
        description="Geographical latitude coordinate",
    )
    lon: Optional[float] = Field(
        default=None,
        description="Geographical longitude coordinate",
    )
    fecha: Optional[datetime] = Field(
        default=None,
        description="Publication timestamp in ISO format",
    )
    enlace: str = Field(
        default="",
        description="External URL pointing to the detailed report",
    )