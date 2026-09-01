# Integración NEXO × GeoRisk — Unidad sin legacy (directrices NEXO)

> **Función NEXO manda:** mapa como protagonista, activación por gestor **ALTO RIESGO** que desbloquea necesidades/ayudas por zona, mensajes en español, código en inglés, una migración por cambio, ER como fuente única. GeoRisk aporta técnica, no cambia función.

## Qué nos quedamos (lo mejor de cada uno)

### De NEXO (estructura y función)
- **Sprint 2 G1-G4:** G1 Necesidades (8 cats/2 estados + `direccion` + `services.py` + `geocodificacion.js` — ya en `dev` 91a7647), G2 Alertas (RiskLevelEnum + `zone` GeoJSON, rama `alerts`), G3 Ayudas (wrapper `POST /api/ayudas`), G4 Mapa (capas + intensidad 🟢🟠🔴)
- **Contratos mapa:** `alerta→{id,risk_level,status,zone}`, `necesidad→{id,type,lat,lon,status,direccion}`, `ayuda→{id,type,category,lat,lon,status}`
- **Trazabilidad:** `docs/modelo-entidad-relacion.md` (ER SQLite, 1 FK real), `docs/backlog.md` (Sprint 1 histórico + Sprint 2 actual), Kanban idempotente `scripts/setup-kanban.sh` (fix matching exacto ya en `docs/trazabilidad-2026-08-31`)
- **Jamstack Vercel:** `api/index.py` reexporta `backend/main:app` + `vercel.json` (ya en `integration/nexo-georisk` 4f9f29f) — abandona Streamlit Cloud
- **Convenciones:** código inglés, comentarios/docs español, vertical por módulo, `main` protegida, `dev` integración

### De GeoRisk (técnica útil, sin cambiar función)
- **H3 (`src/h3_aggregator.py`):** `lat_lon_to_h3`, `aggregate_by_h3`, `merge_h3_datasets` — para **intensidad por hex** y `zone` discreta (res 6-7). Mantiene función NEXO (ALTO RIESGO sigue siendo interruptor), solo optimiza cálculo de zona.
- **Globo (`georisk_globe/frontend/`):** `index.html` + `layer_panel/` + `click_reader/` — reservado para **toggle post-MVP** (`?globe=1`), no para demo Jueves. Mantiene mapa 2D NEXO como protagonista.
- **Clustering/visualización (`src/clustering.py`, `src/visualization.py:plot_risk_map`):** solo como referencia de estilo (paleta `mako`, `CartoDB positron`), no se porta Folium a Vercel (se usa MapLibre ya en NEXO).

### Qué descartamos (basura legacy verificada)
- `sync_log` (solo `sync_operations`), `streamlit_app/` (sustituido por Vercel), `notebooks/figures/*.png` + `outputs/figures/*` duplicados, `data/processed/*.csv` pesados (se regeneran con `src/data_loader.py`), `app/app_informes` vacío, `backend_server.err`/`frontend_server.err`.

## Esquema unificado Alertas (GeoRisk como fuente única)

```python
# NEXO `schemas.py` actual: fuente/tipo/severidad/pais/lat/lon (punto)
# Nuevo (src/features/alerts/schemas.py) siguiendo directrices NEXO (inglés en código):
{
    "external_id": "GDACS_1234",  # evita colisión IDs locales
    "title": str, "event_type": "terremoto|...", "source": "GDACS|PROTECCION_CIVIL|MANUAL",
    "severity": "RED|ORANGE|GREEN", "risk_level": "low|medium|high",
    "status": "normal|active|high_risk|deactivated", "zone": GeoJSON, "is_active": bool,
    "h3_cells": list[str]  # derivado de zone vía h3_aggregator (res 6)
}
```
- Ingesta única en GeoRisk: `fetch_and_normalize_gdacs()` → NEXO solo consume, deduplica por `external_id`, fallback `[]` sin 500 (ya en `gdacs_client.py`).

## Estructura final limpia (Vercel)

```
api/index.py          # Serverless FastAPI (reexporta backend/main:app)
public/index.html     # CDN estático (NEXO frontend + toggle globo)
backend/              # NEXO: modules/necesidades, alertas, donaciones, personas, sync
frontend/             # NEXO: pages/mapa.html, js/core/mapa-necesidades (Leaflet/MapLibre)
src/h3_aggregator.py  # GeoRisk: solo este archivo + h3 (no notebooks)
georisk_globe/frontend/ # GeoRisk: solo para toggle post-MVP
vercel.json           # rewrites /api/* -> api/index.py
docs/                 # trazabilidad Sprint 1-2 + ER
```

## Flujo demo Jueves (sin legacy)
Gestor crea alerta → delimita `zone` (polígono) → ALTO RIESGO → `h3_cells` derivados → mapa resalta zona → necesidades/ayudas filtradas por `h3` aparecen con intensidad → marcar cubierta.

> Próximo paso en ramas personales (no `main`): P1 Javi G2 `zone`+`external_id`, P2 Luis G1 `direccion`, P3 Vanessa G3 `ayudas`, P4 Juan G4 capas + H3 intensidad + toggle globo.
