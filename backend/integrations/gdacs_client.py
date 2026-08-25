"""Cliente para GDACS — fuente principal de alertas a nivel mundial"""
import time
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

import requests

from config import GDACS_API_URL, GDACS_CACHE_TTL_SECONDS

_NS = {
    "gdacs": "http://www.gdacs.org",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
}

_EVENT_TYPES = {
    "TC": "ciclon",
    "EQ": "terremoto",
    "FL": "inundacion",
    "WF": "incendio",
    "VO": "volcan",
    "DR": "sequia",
}

_cache = {}


def _map_event_type(event_code):
    return _EVENT_TYPES.get((event_code or "").upper(), "otro")


def _map_severity(alert_level):
    value = (alert_level or "").strip().lower()
    return value if value in ("red", "orange", "green") else "green"


def _get_text(item, tag):
    element = item.find(tag, _NS)
    if element is not None and element.text:
        return element.text.strip()
    return None


def _get_coordinate(item, tag):
    value = _get_text(item, tag)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _to_iso_date(pub_date):
    if not pub_date:
        return None
    try:
        return parsedate_to_datetime(pub_date)
    except (TypeError, ValueError):
        return None


def _parse_item(item):
    event_type = _get_text(item, "gdacs:eventtype")
    event_id = _get_text(item, "gdacs:eventid")
    alert_level = _get_text(item, "gdacs:alertlevel")
    country = _get_text(item, "gdacs:country")

    lat = _get_coordinate(item, "geo:Point/geo:lat")
    if lat is None:
        lat = _get_coordinate(item, "geo:lat")
    if lat is None:
        lat = 0.0

    lon = _get_coordinate(item, "geo:Point/geo:long")
    if lon is None:
        lon = _get_coordinate(item, "geo:long")
    if lon is None:
        lon = 0.0

    fecha = _to_iso_date(_get_text(item, "pubDate"))
    if fecha is None:
        fecha = datetime.now(timezone.utc)

    return {
        "id": f"gdacs-{event_type or 'NA'}{event_id or ''}",
        "fuente": "gdacs",
        "tipo": _map_event_type(event_type),
        "titulo": _get_text(item, "title") or "Sin título",
        "descripcion": _get_text(item, "description") or "",
        "severidad": _map_severity(alert_level),
        "pais": country or "",
        "lat": lat,
        "lon": lon,
        "fecha": fecha,
        "enlace": _get_text(item, "link") or "",
    }


def _download_and_parse():
    response = requests.get(GDACS_API_URL, timeout=10)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = root.findall(".//item")

    return [_parse_item(item) for item in items]


def get_alerts():
    # Campos en español: contrato de datos acordado con services.py/routes.py
    now = time.time()
    cached_entry = _cache.get("alerts")

    if cached_entry is not None:
        previous_timestamp, previous_alerts = cached_entry
        if now - previous_timestamp < GDACS_CACHE_TTL_SECONDS:
            return previous_alerts

    try:
        alerts = _download_and_parse()
    except (requests.RequestException, ET.ParseError):
        return []

    _cache["alerts"] = (now, alerts)
    return alerts