"""API router for alert endpoints."""

from typing import Dict, List, Optional
from fastapi import APIRouter, Query
from modules.alertas.schemas import AlertResponse, EventTypeEnum, SeverityEnum
from modules.alertas.services import list_filtered_alerts

router = APIRouter(prefix="/api/alertas", tags=["alertas"])


@router.get("", response_model=List[AlertResponse])
def get_alertas(
    tipo: Optional[EventTypeEnum] = Query(None, description="Filter by event type"),
    severidad: Optional[SeverityEnum] = Query(None, description="Filter by severity level"),
    pais: Optional[str] = Query(None, description="Filter by country substring"),
) -> List[Dict]:
    """Retrieves official disaster alerts with optional parameter filtering.

    Guarantees an HTTP 200 status code with an empty JSON list if no records
    match or if external integrations fail.

    Args:
        tipo (Optional[EventTypeEnum]): Event classification query.
        severidad (Optional[SeverityEnum]): Severity tier query.
        pais (Optional[str]): Target country query.

    Returns:
        List[Dict]: Processed alert dictionaries automatically validated by FastAPI.
    """
    tipo_val = tipo.value if tipo else None
    severidad_val = severidad.value if severidad else None

    return list_filtered_alerts(tipo=tipo_val, severidad=severidad_val, pais=pais)