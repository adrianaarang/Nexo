"""Business logic, data aggregation, and query filtering for alerts."""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

from integrations import gdacs_client, gdacs_mock, proteccion_civil_client

logger = logging.getLogger(__name__)

# Mapa de paises en espanol -> nombre que usa GDACS (ingles) para el filtrado.
COUNTRY_ALIASES = {
    "españa": "spain",
    "espana": "spain",
    "francia": "france",
    "italia": "italy",
    "grecia": "greece",
    "turquia": "turkey",
    "turquía": "turkey",
    "marruecos": "morocco",
    "portugal": "portugal",
    "alemania": "germany",
    "reino unido": "united kingdom",
    "estados unidos": "united states",
    "argentina": "argentina",
    "chile": "chile",
    "mexico": "mexico",
    "méxico": "mexico",
    "colombia": "colombia",
    "peru": "peru",
    "brasil": "brazil",
}


def fetch_base_alerts() -> List[Dict[str, Any]]:
    """Retrieves raw alert items from GDACS and Proteccion Civil integrations.

    Falls back to the internal mock dataset if external sources are unavailable,
    fail during invocation, or return empty results.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing raw alert entities.
    """
    alerts: List[Dict[str, Any]] = []

    try:
        gdacs_data = gdacs_client.get_alerts()
        if gdacs_data:
            alerts.extend(gdacs_data)
    except Exception as exc:
        logger.error("Failed to fetch alerts from GDACS client: %s", exc, exc_info=True)

    try:
        pc_data = proteccion_civil_client.get_alerts()
        if pc_data:
            alerts.extend(pc_data)
    except Exception as exc:
        logger.error("Failed to fetch alerts from Proteccion Civil client: %s", exc, exc_info=True)

    if alerts:
        return alerts

    logger.warning("No external alerts retrieved. Falling back to internal mock dataset.")
    return getattr(gdacs_mock, "MOCK_GDACS_DATA", [])


def list_filtered_alerts(
    tipo: Optional[str] = None,
    severidad: Optional[str] = None,
    pais: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filters and sorts alert records based on specified query parameters.

    Args:
        tipo (Optional[str]): Target event type filter (e.g., "terremoto").
        severidad (Optional[str]): Severity level filter (e.g., "red").
        pais (Optional[str]): Case-insensitive substring match for country name.

    Returns:
        List[Dict[str, Any]]: Processed alerts sorted in descending chronological order.
    """
    alerts: List[Dict[str, Any]] = fetch_base_alerts()

    # Pre-limpieza de argumentos para evitar repetición en el bucle
    tipo_clean = tipo.strip().lower() if tipo and tipo.strip() else None
    severidad_clean = severidad.strip().lower() if severidad and severidad.strip() else None
    search_term = pais.strip().lower() if pais and pais.strip() else None
    if search_term:
        search_term = COUNTRY_ALIASES.get(search_term, search_term)

    # Filtrado unificado en una sola pasada
    filtered_alerts = []
    for item in alerts:
        if tipo_clean and item.get("tipo", "").lower() != tipo_clean:
            continue
        if severidad_clean and item.get("severidad", "").lower() != severidad_clean:
            continue
        if search_term and search_term not in (item.get("pais") or "").lower():
            continue
        filtered_alerts.append(item)

    min_utc_date = datetime.min.replace(tzinfo=timezone.utc)

    def extract_sorting_key(item: Dict[str, Any]) -> datetime:
        dt = item.get("fecha")
        if not isinstance(dt, datetime):
            return min_utc_date
        return dt if dt.tzinfo is not None else dt.replace(tzinfo=timezone.utc)

    filtered_alerts.sort(key=extract_sorting_key, reverse=True)
    return filtered_alerts