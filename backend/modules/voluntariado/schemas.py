"""Validación de entrada/salida de voluntarios.

Los nombres de Python siguen la convención técnica en inglés. Los alias en
español conservan el contrato JSON ya compartido con el equipo de frontend.
"""
from datetime import date, datetime
from enum import Enum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"


class VolunteerStatus(str, Enum):
    """Estados del ciclo de validación de un voluntario."""

    PENDING = "pendiente"
    APPROVED = "aprobado"
    REJECTED = "rechazado"


class CoordinationStatus(str, Enum):
    """Estado operativo visible en el frontend."""

    AVAILABLE = "available"
    ASSIGNED = "assigned"
    RESTING = "resting"


class TransportationType(str, Enum):
    OWN_VEHICLE = "own_vehicle"
    NEEDS_TRANSPORT = "needs_transport"


class VehicleType(str, Enum):
    CAR = "car"
    VAN = "van"
    FOUR_BY_FOUR = "four_by_four"


class VolunteerTask(str, Enum):
    DONATION_SORTING = "donation_sorting"
    SUPPLY_DISTRIBUTION = "supply_distribution"
    LIGHT_DEBRIS_CLEANUP = "light_debris_cleanup"
    VULNERABLE_PERSON_SUPPORT = "vulnerable_person_support"
    TELEPHONE_INFORMATION = "telephone_information"
    RESCUED_ANIMAL_CARE = "rescued_animal_care"
    ANY_ASSIGNED_TASK = "any_assigned_task"


class VolunteerCertification(str, Enum):
    DOCTOR = "doctor"
    NURSE = "nurse"
    NURSING_ASSISTANT = "nursing_assistant"
    PSYCHOLOGIST = "psychologist"
    FIRST_AID = "first_aid"
    FORKLIFT_LICENSE = "forklift_license"
    FOOD_HANDLER = "food_handler"
    COOK = "cook"
    DRIVING_LICENSE_B = "driving_license_b"
    DRIVING_LICENSE_C = "driving_license_c"
    VETERINARIAN = "veterinarian"
    SOCIAL_WORKER = "social_worker"
    TRANSLATOR = "translator"


class AvailabilitySlot(BaseModel):
    """Franja horaria concreta de disponibilidad."""

    model_config = ConfigDict(extra="forbid")

    starts_at: datetime


def _validate_dni(value: str) -> str:
    normalized = value.strip().upper()
    if len(normalized) != 9 or not normalized[:8].isdigit() or not normalized[8].isalpha():
        raise ValueError("El DNI debe tener 8 números y una letra de control.")
    expected = DNI_LETTERS[int(normalized[:8]) % 23]
    if normalized[8] != expected:
        raise ValueError("La letra de control del DNI no es válida.")
    return normalized


class VolunteerFrontendCreate(BaseModel):
    """Entrada JSON del formulario de voluntariado."""

    model_config = ConfigDict(extra="forbid")

    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=150)
    dni: str = Field(min_length=9, max_length=9)
    birth_date: date
    phone: str = Field(min_length=3, max_length=30)
    locality: str = Field(min_length=2, max_length=120)
    tasks: list[VolunteerTask] = Field(min_length=1)
    certifications: list[VolunteerCertification] = Field(default_factory=list)
    transportation: TransportationType
    vehicle_type: VehicleType | None = None
    availability_slots: list[AvailabilitySlot] = Field(default_factory=list)
    skills: str | None = Field(default=None, max_length=250)

    @field_validator("first_name", "last_name", "phone", "locality", "skills", mode="before")
    @classmethod
    def strip_optional_text(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("dni", mode="before")
    @classmethod
    def normalize_dni(cls, value: object) -> object:
        if isinstance(value, str):
            return _validate_dni(value)
        return value

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("La fecha de nacimiento no puede estar en el futuro.")
        return value

    @field_validator("availability_slots")
    @classmethod
    def validate_availability_slots(
        cls,
        slots: list[AvailabilitySlot],
    ) -> list[AvailabilitySlot]:
        for slot in slots:
            starts_at = slot.starts_at

            if starts_at.tzinfo is None:
                current_time = datetime.now()
            else:
                current_time = datetime.now(starts_at.tzinfo)

            if starts_at < current_time:
                raise ValueError(
                    "Las franjas de disponibilidad no pueden estar en el pasado."
                )

        return slots

    @model_validator(mode="after")
    def validate_vehicle_type(self) -> Self:
        if (
            self.transportation == TransportationType.OWN_VEHICLE
            and self.vehicle_type is None
        ):
            raise ValueError("vehicle_type es obligatorio con own_vehicle.")

        if self.transportation == TransportationType.NEEDS_TRANSPORT:
            self.vehicle_type = None

        return self


class VolunteerFrontendResponse(BaseModel):
    """Representación pública del contrato frontend."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    first_name: str
    last_name: str
    full_name: str
    locality: str
    tasks: list[str]
    certifications: list[str] = Field(default_factory=list)
    transportation: str = ""
    vehicle_type: str | None = None
    availability_slots: list[AvailabilitySlot] = Field(default_factory=list)
    skills: str = ""
    status: CoordinationStatus


class VolunteerFrontendRegistrationResponse(VolunteerFrontendResponse):
    """Respuesta del registro JSON con datos personales adicionales."""

    dni: str
    birth_date: date
    phone: str


class VolunteerCoordinationUpdate(BaseModel):
    """Entrada para actualizar el estado operativo."""

    model_config = ConfigDict(extra="forbid")

    status: CoordinationStatus


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
