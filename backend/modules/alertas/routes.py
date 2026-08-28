"""API router for alert endpoints."""
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from modules.alertas.schemas import (
    AlertResponse,
    AlertCreate,
    AlertUpdate,
    EventTypeEnum,
    SeverityEnum,
)
from modules.alertas import services
from modules.alertas.models import (
    create_alert,
    get_alert,
    update_alert,
    set_activation,
)

router = APIRouter(prefix="/api/alertas", tags=["alertas"])


def _not_found(alert_id: int) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Alerta {alert_id} no encontrada",
    )


@router.get("", response_model=List[AlertResponse])
def get_alertas(
    tipo: Optional[str] = Query(None, description="Filter by event type"),
    severidad: Optional[str] = Query(None, description="Filter by severity level"),
    pais: Optional[str] = Query(None, description="Filter by country substring"),
) -> List[Dict]:
    """Lista alertas externas (GDACS/PC) y del gestor en una sola respuesta.

    Garantiza HTTP 200 con lista (vacía si no hay coincidencias o fallan
    las integraciones externas).
    """
    tipo_clean = tipo.strip() if tipo and tipo.strip() else None
    severidad_clean = severidad.strip() if severidad and severidad.strip() else None
    pais_clean = pais.strip() if pais and pais.strip() else None

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

    return services.combined_alerts(
        tipo=tipo_clean,
        severidad=severidad_clean,
        pais=pais_clean,
    )


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def crear_alerta(payload: AlertCreate) -> Dict:
    """Crea una alerta del gestor (inactiva por defecto) y devuelve su estado."""

    row = create_alert(payload)
    return services.gestor_row_to_response(row, include_token=True)


@router.get("/{alert_id}", response_model=AlertResponse)
def obtener_alerta(alert_id: int) -> Dict:
    """Devuelve una alerta del gestor por id (404 si no existe)."""

    row = get_alert(alert_id)
    if row is None:
        raise _not_found(alert_id)
    return services.gestor_row_to_response(row, include_token=True)


@router.patch("/{alert_id}", response_model=AlertResponse)
def actualizar_alerta(alert_id: int, payload: AlertUpdate) -> Dict:
    """Actualiza campos editables de una alerta del gestor (404 si no existe)."""

    row = update_alert(alert_id, payload)
    if row is None:
        raise _not_found(alert_id)
    return services.gestor_row_to_response(row, include_token=True)


@router.post("/{alert_id}/activar", response_model=AlertResponse)
def activar_alerta(alert_id: int) -> Dict:
    """Activa una alerta del gestor (estado active). Idempotente."""

    row = set_activation(alert_id, True)
    if row is None:
        raise _not_found(alert_id)
    return services.gestor_row_to_response(row)


@router.post("/{alert_id}/alto-riesgo", response_model=AlertResponse)
def alto_riesgo_alerta(alert_id: int) -> Dict:
    """Marca la alerta como ALTO RIESGO: fija nivel='alto' y la activa."""

    row = set_activation(alert_id, True, alto_riesgo=True)
    if row is None:
        raise _not_found(alert_id)
    return services.gestor_row_to_response(row)


@router.post("/{alert_id}/desactivar", response_model=AlertResponse)
def desactivar_alerta(alert_id: int) -> Dict:
    """Desactiva una alerta del gestor (estado inactive). Idempotente."""

    row = set_activation(alert_id, False)
    if row is None:
        raise _not_found(alert_id)
    return services.gestor_row_to_response(row)
