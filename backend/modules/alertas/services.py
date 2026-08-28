"""Business logic, data aggregation, and query filtering for alerts."""

import json
from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

from integrations import gdacs_client, gdacs_mock, proteccion_civil_client
from modules.alertas import models

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


# ---------------------------------------------------------------------------
# Alertas del gestor (persistidas en la tabla `alertas`)
# ---------------------------------------------------------------------------

SEVERITY_TO_RISK = {"red": "alto", "orange": "medio", "green": "bajo"}


def _parse_zona(raw: Any) -> Optional[Dict[str, Any]]:
    """Convierte el GeoJSON guardado como texto en dict, o None si no es válido."""

    if not raw:
        return None
    if isinstance(raw, dict):
        return raw
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else None
    except (json.JSONDecodeError, TypeError):
        return None


def gestor_row_to_response(row: Dict[str, Any], include_token: bool = False) -> Dict[str, Any]:
    """Convierte una fila SQLite de alerta del gestor en el formato de respuesta.

    Calcula ``status`` (inactive/active/alto_riesgo) y expone ``risk_level`` /
    ``zone`` para el contrato del mapa. El ``gestor_token`` solo se incluye
    cuando ``include_token`` es True (creación y consulta individual).
    """

    zona = _parse_zona(row.get("zona"))
    activa = bool(row.get("activa"))
    nivel = row.get("nivel_riesgo")

    if activa and nivel == "alto":
        estado = "alto_riesgo"
    elif activa:
        estado = "active"
    else:
        estado = "inactive"

    return {
        "id": str(row.get("id")),
        "fuente": row.get("fuente") or "gestor",
        "tipo": row.get("tipo"),
        "titulo": row.get("titulo") or "",
        "descripcion": row.get("descripcion") or "",
        "severidad": None,
        "pais": None,
        "lat": row.get("latitud"),
        "lon": row.get("longitud"),
        "fecha": None,
        "enlace": None,
        "nivel_riesgo": nivel,
        "zona": zona,
        "activa": activa,
        "gestor_token": row.get("gestor_token") if include_token else None,
        "risk_level": nivel,
        "status": estado,
        "zone": zona,
    }


def _enrich_gdacs_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Añade risk_level/status/zone a una alerta externa para el contrato del mapa."""

    enriched = dict(item)
    sev = (item.get("severidad") or "").lower()
    enriched["risk_level"] = SEVERITY_TO_RISK.get(sev)
    enriched["status"] = "active"
    enriched["zone"] = None
    return enriched


def combined_alerts(
    tipo: Optional[str] = None,
    severidad: Optional[str] = None,
    pais: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Une alertas externas (GDACS/PC) y alertas del gestor en una sola lista.

    Las alertas externas se filtran por los parámetros recibidos; las del
    gestor se filtran solo por ``tipo`` cuando aplique.
    """

    gdacs = list_filtered_alerts(tipo=tipo, severidad=severidad, pais=pais)
    result = [_enrich_gdacs_item(item) for item in gdacs]

    try:
        gestor_rows = models.list_alerts()
    except Exception as exc:  # Tabla aún no existe o BD no accesible
        logger.warning("No se pudieron leer alertas del gestor: %s", exc)
        gestor_rows = []

    for row in gestor_rows:
        if tipo and (row.get("tipo") or "") != tipo:
            continue
        result.append(gestor_row_to_response(row))

    return result