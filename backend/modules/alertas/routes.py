"""API router for alert endpoints."""

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from modules.alertas.schemas import AlertResponse, EventTypeEnum, SeverityEnum
from modules.alertas.services import list_filtered_alerts

router = APIRouter(prefix="/api/alertas", tags=["alertas"])


@router.get("", response_model=List[AlertResponse])
def get_alertas(
    tipo: Optional[str] = Query(None, description="Filter by event type"),
    severidad: Optional[str] = Query(None, description="Filter by severity level"),
    pais: Optional[str] = Query(None, description="Filter by country substring"),
) -> List[Dict]:
    """Retrieves official disaster alerts with optional parameter filtering.

    Guarantees an HTTP 200 status code with an empty JSON list if no records
    match or if external integrations fail.

    - Args:
        - tipo (Optional[str]): Event classification query.
        - severidad (Optional[str]): Severity tier query.
        - pais (Optional[str]): Target country query.

    - Returns:
        - List[Dict]: Processed alert dictionaries automatically validated by FastAPI.
    """
    # Sanitize empty string queries to None to allow empty query string parameters
    tipo_clean = tipo.strip() if tipo and tipo.strip() else None
    severidad_clean = severidad.strip() if severidad and severidad.strip() else None
    pais_clean = pais.strip() if pais and pais.strip() else None

    # Validate against Enums manually if a non-empty string value was supplied
    if tipo_clean:
        try:
            EventTypeEnum(tipo_clean)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid event type: {tipo_clean}",
            )

    if severidad_clean:
        try:
            SeverityEnum(severidad_clean)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid severity level: {severidad_clean}",
            )

    return list_filtered_alerts(
        tipo=tipo_clean,
        severidad=severidad_clean,
        pais=pais_clean,
    )