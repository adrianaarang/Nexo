"""Isolated mock dataset for GDACS alerts testing and local development."""

from datetime import datetime, timezone
from typing import Any, Dict, List

MOCK_GDACS_DATA: List[Dict[str, Any]] = [
    {
        "id": "gdacs-FL20260002",
        "fuente": "gdacs",
        "tipo": "inundacion",
        "titulo": "Flood - Spain",
        "descripcion": "Severe flooding in the Ebro river basin",
        "severidad": "red",
        "pais": "Spain",
        "lat": 41.65,
        "lon": -0.88,
        "fecha": datetime(2026, 4, 30, 13, 7, 47, tzinfo=timezone.utc),
        "enlace": "https://www.gdacs.org/report.aspx?eventid=1002",
    },
    {
        "id": "gdacs-EQ20260001",
        "fuente": "gdacs",
        "tipo": "terremoto",
        "titulo": "Earthquake - Spain",
        "descripcion": "Magnitude 4.2 earthquake in Granada",
        "severidad": "green",
        "pais": "Spain",
        "lat": 37.17,
        "lon": -3.60,
        "fecha": datetime(2026, 4, 29, 8, 30, 0, tzinfo=timezone.utc),
        "enlace": "https://www.gdacs.org/report.aspx?eventid=1001",
    },
    {
        "id": "gdacs-TC20260003",
        "fuente": "gdacs",
        "tipo": "ciclon",
        "titulo": "Tropical Cyclone - Philippines",
        "descripcion": "Tropical cyclone approaching the coastline",
        "severidad": "orange",
        "pais": "Philippines",
        "lat": 12.87,
        "lon": 121.77,
        "fecha": datetime(2026, 4, 28, 10, 0, 0, tzinfo=timezone.utc),
        "enlace": "https://www.gdacs.org/report.aspx?eventid=1003",
    },
]