# Grupo 2 — Alertas Oficiales · Plan de trabajo y reparto

- **Integrantes:** Joel, Juan (PO), Luis, Javi y Vanessa
- **Módulo:** Alertas oficiales (núcleo del MVP)
- **Fecha:** 19/08/2026

## 0. ¿Podemos empezar ya?
Sí. La base común ya está montada (Adriana) y el router de alertas ya está registrado en
`backend/main.py`. No dependemos de directrices pendientes de otros equipos y no bloqueamos a
nadie. Solo hay 4 decisiones de producto cerradas (sección 3) que hay que respetar.

## 1. Especificaciones del repo
- **Arranque:** ver `README.md` (backend puerto 8000, frontend puerto 5500).
- **Dependencias instaladas (no añadir nuevas sin justificar):** `fastapi`, `uvicorn[standard]`,
  `pydantic`, `requests` (RSS de GDACS), `python-dotenv`. Parseo con `xml.etree.ElementTree` (stdlib).
- **Archivos del módulo:**
  | Qué | Ruta |
  |-----|------|
  | Cliente GDACS (fuente principal) | `backend/integrations/gdacs_client.py` |
  | Capa local Protección Civil (TODO) | `backend/integrations/proteccion_civil_client.py` |
  | Lógica del módulo | `backend/modules/alertas/services.py` |
  | Endpoints | `backend/modules/alertas/routes.py` |
  | Página de alertas | `frontend/pages/alertas.html` |
  | Render de alertas | `frontend/js/core/alertas-oficiales/alertas.js` |
  | Llamadas al backend | `frontend/js/core/alertas-oficiales/alertasApi.js` |
  | Tests backend | `tests/backend/test_alertas.py` (crear) |
  | Test frontend | `tests/frontend/alertas.test.js` (crear) |
- **Base común a importar (no reimplementar):** `apiClient.js` (`apiGet`), `utils.js`
  (`formatDate`, `el`), `components/card.js` (`crearTarjeta`), `app.js`, `components/header.js`,
  `index.html` (patrón), CSS compartido (`variables.css`, `components.css`).
- **Config (`backend/config.py`):** `GDACS_API_URL`, `PROTECCION_CIVIL_API_URL` (vacía),
  `GDACS_CACHE_TTL_SECONDS = 900` (15 min).
- **BD:** no se necesitan tablas nuevas; el caché va en memoria. No tocar `001_init.sql`.
- **CI:** `.github/workflows/ci.yml` ejecuta `pytest` en `backend/` (debe pasar en verde).
- **Git:** rama `feature/alertas-oficiales`; PR pequeño; commits describiendo prioridad (núcleo).

## 2. Estado actual del módulo
Todos los archivos del módulo estaban pendientes/VACÍOS salvo `routes.py` (solo el router sin
endpoint). *(Nota PM: en `origin/feature/alerts` ya hay backend completo; ver `docs/backlog.md`.)*

## 3. Decisiones de producto (cerradas con el PO) — D1 a D4
- **D1 — Caché GDACS:** Sí, en memoria, TTL 15 min. Resuelve el bloqueo por muchas llamadas.
- **D2 — Sin alertas activas:** estado vacío *"Sin alertas activas ahora"* + fecha de última
  actualización + fuentes consultadas.
- **D3 — Filtros:** por tipo de evento, severidad y país (por defecto: todos).
- **D4 — Protección Civil:** se DEJA DOCUMENTADO como TODO (no es AEMET ni IGN). Nos centramos en GDACS.

> Estas decisiones se registran aquí inline; se promueven a ADR separados (`docs/adr/`) solo si la comisión lo pide.

## 4. Modelo de datos de una alerta (formato interno Nexo)
```json
{
  "id": "gdacs-EQ2026xxxxx",
  "fuente": "gdacs",
  "tipo": "terremoto",
  "titulo": "Earthquake ...",
  "descripcion": "...",
  "severidad": "red",
  "pais": "Espania",
  "lat": 39.4, "lon": -0.3,
  "fecha": "2026-08-19T10:00:00Z",
  "enlace": "https://www.gdacs.org/..."
}
```
- **Tipos:** terremoto | ciclon | inundacion | incendio | volcan | sequia | otro
- **Severidades:** red | orange | green
- **Mapeo GDACS:** TC=ciclón, EQ=terremoto, FL=inundación, WF=incendio, VO=volcán, DR=sequía
- **Contrato API:** `GET /api/alertas?tipo=&severidad=&pais=` → `200 [{...}]` ordenadas por fecha
  (más reciente primero) · `200 []` si no hay alertas o GDACS falla (nunca 500).

## 5. Reparto por persona (archivos EXCLUSIVOS)
| Persona | Entrega | Archivos | Cómo probar sin dependientes |
|---------|---------|----------|------------------------------|
| LUIS | A1 Cliente GDACS + A2 Caché TTL | `gdacs_client.py` + `config.py` | Script: parsea RSS real → lista |
| JAVI | A3 Servicio/filtros + A4 Ruta + C1 Tests | `services.py` + `routes.py` + `tests/backend/test_alertas.py` | Trabaja contra firma `get_alertas()` con mock; pytest verde |
| JUAN | B1 Cliente API + B3 estados + C4 Revisión/merge | `alertasApi.js` + `estadosAlertas.js` (nuevo) | Código contra JSON mock; render de estados sin backend |
| JOEL | B2 Pantalla + B3 render/filtros + C3 Demo | `alertas.html` + `alertas.js` | La página carga y muestra el mock sin backend |
| VANESSA | B4 Estilos + C2 Test frontend | `css/alertas.css` (nuevo) + `tests/frontend/alertas.test.js` | Test con datos de ejemplo, sin API viva |

**Regla de paralelismo:** cada persona trabaja SOLO en sus archivos contra un mock/JSON de ejemplo
con la misma forma del contrato. Un solo punto de unión al final (integración corta).

## 6. Definición de "Hecho" (Done)
1. Implementado según arquitectura del repo.
2. `pytest` en `backend/` en verde.
3. No rompe funcionalidades de otros módulos.
4. Revisado en PR (revisión de al menos otra persona del grupo).
5. Demostrable en la demo (caso C3).

## 7. Reglas para no pisar a otros equipos
- NO tocar: `main.py`, `001_init.sql`, `apiClient.js`, CSS compartidos, archivos de otros módulos.
- Rama `feature/alertas-oficiales`. No añadir dependencias sin consultar.

## 8. Fuera de alcance del Grupo 2
Tablas nuevas en BD (caché en memoria); AEMET/IGN/protocolos de Protección Civil; simulación, IA,
what-if, índices de resiliencia; dependencias nuevas.

## 9. Preguntas abiertas (no bloquean, resolver en daily)
- ¿GitHub Projects o Trello para el backlog del equipo?
- ¿El mapa de alertas geolocalizadas queda para después? (por ahora: lista)
