from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DonationType(str, Enum):
    OFFERED = "ofrecida"
    REQUESTED = "solicitada"


class DonationStatus(str, Enum):
    ACTIVE = "activa"
    DELIVERED = "entregada"


class DonationResource(str, Enum):
    WATER = "Agua"
    FOOD = "Comida"
    BLANKETS = "Mantas"
    CHILDREN_CLOTHING = "Ropa infantil"
    ADULT_CLOTHING = "Ropa de adultos"
    HYGIENE_PRODUCTS = "Productos de higiene"
    TEMPORARY_SHELTER = "Alojamiento temporal"
    FUEL_OR_BATTERIES = "Combustible y/o baterías"
    COMMUNICATION_SERVICES = "Servicios de comunicación"
    MEDICATIONS = "Medicamentos"
    FIRST_AID_SUPPLIES = "Material de primeros auxilios"
    BABY_ITEMS = "Artículos para bebés"
    TOOLS = "Herramientas"
    TRANSPORT = "Transporte"
    BEVERAGES = "Bebidas"
    OTHER = "Otros"


class DonationBase(BaseModel):
    # populate_by_name permite construir el modelo tanto con el nombre
    # Python (en inglés) como con el alias (en español, el contrato JSON).
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    donation_type: DonationType = Field(alias="tipo")
    resource: DonationResource = Field(alias="recurso")
    quantity: str = Field(default="", max_length=100, alias="cantidad")
    description: str = Field(default="", max_length=1000, alias="descripcion")
    contact: str = Field(min_length=3, max_length=200, alias="contacto")

    @field_validator("contact", mode="before")
    @classmethod
    def normalize_text(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value


class DonationCreate(DonationBase):
    pass


class DonationStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    status: DonationStatus = Field(alias="estado")


class DonationResponse(DonationBase):
    id: int = Field(gt=0)
    status: DonationStatus = Field(alias="estado")
    created_at: datetime = Field(alias="creado_en")