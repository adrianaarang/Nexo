# Nexo — Conectados para ayudarnos

# Nexo — Connected to help each other

App comunitaria de respuesta a emergencias y desastres naturales: mapa de necesidades en tiempo real, alertas oficiales, voluntariado y donaciones. Registro de personas y modo sin conexión como siguientes prioridades. Red mesh/satélite y código abierto quedan como roadmap futuro.

Community app for emergency and natural-disaster response: real-time needs map, official alerts, volunteering and donations. Person registry and offline mode as next priorities. Mesh/satellite network and open source remain future roadmap.

Alcance decidido por votación de equipo — ver `docs/decisiones-encuesta.md` y `docs/roadmap.md`.

Scope decided by team vote — see `docs/decisiones-encuesta.md` and `docs/roadmap.md`.

## Estructura / Structure

- `frontend/` — HTML, CSS y JS (PWA).
- `backend/` — API en Python (FastAPI).
- `docs/` — decisiones de producto, arquitectura y privacidad.
- `infra/` — notas de infraestructura futura (red mesh/satélite).

EN:

- `frontend/` — HTML, CSS and JS (PWA).
- `backend/` — Python API (FastAPI).
- `docs/` — product decisions, architecture and privacy.
- `infra/` — future infrastructure notes (mesh/satellite network).

## Documentación de gobernanza / Governance documentation

- `docs/manifiesto.md` — visión, principios, objetivos MVP y organización del proyecto.
- `docs/convenciones.md` — reglas de equipo (ramas, commits, PRs, ADRs, propiedad de archivos).
- `docs/reparto-trabajo.md` — reparto en 4 equipos y base común.
- `docs/formas-de-trabajo.md` — acuerdos de equipo (Trello, estilos, alcance, PRs).
- `docs/roles-y-tareas.md` — roles y división de tareas por grupo (cada SM completa su sección).
- `docs/faq.md` — preguntas frecuentes y decisiones curadas (Grupo 2 y Grupo 4).
- `docs/backlog.md` — estado por módulo y pendientes de gobernanza (mantenido por el PM).
- `docs/equipos.md` — composición de los 4 equipos y mapeo a bloques del Kanban.
- `docs/equipos/grupo2-alertas.md` — plan de trabajo de Alertas Oficiales (Grupo 2).
- `docs/equipos/grupo2-tareas.md` — guion de reunión y checklist del Grupo 2.
- `estructura/` — guías de estructura de archivos (`estructuranexo.md`, `estructuranexoexplicada.md`).

EN:

- `docs/manifiesto.md` — vision, principles, MVP objectives and project organization.
- `docs/convenciones.md` — team rules (branches, commits, PRs, ADRs, file ownership).
- `docs/reparto-trabajo.md` — split into 4 teams and common base.
- `docs/formas-de-trabajo.md` — team agreements (Trello, styles, scope, PRs).
- `docs/roles-y-tareas.md` — roles and task split per group (each SM fills their section).
- `docs/faq.md` — FAQ and curated decisions (Group 2 and Group 4).
- `docs/backlog.md` — per-module status and governance pending items (maintained by PM).
- `docs/equipos.md` — composition of the 4 teams and mapping to Kanban blocks.
- `docs/equipos/grupo2-alertas.md` — work plan for Official Alerts (Group 2).
- `docs/equipos/grupo2-tareas.md` — meeting script and Group 2 checklist.
- `estructura/` — file structure guides (`estructuranexo.md`, `estructuranexoexplicada.md`).

## Cómo arrancar / How to run

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python db/seed.py               # datos de ejemplo / seed sample data
uvicorn main:app --reload --port 8000
```

La API queda disponible en `http://localhost:8000`. Documentación automática en `http://localhost:8000/docs`.

The API is available at `http://localhost:8000`. Auto docs at `http://localhost:8000/docs`.

### Frontend

No necesita build. Sirve la carpeta `frontend/` con cualquier servidor estático, por ejemplo:

No build needed. Serve the `frontend/` folder with any static server, e.g.:

```bash
cd frontend
python -m http.server 5500
```

Abre `http://localhost:5500`. El frontend espera la API en `http://localhost:8000` (configurable en `frontend/js/shared/apiClient.js`).

Open `http://localhost:5500`. The frontend expects the API at `http://localhost:8000` (configurable in `frontend/js/shared/apiClient.js`).

## Módulos / Modules

| Prioridad / Priority | Módulo / Module | Carpeta / Folder | Estado / Status |
|---|---|---|---|
| Núcleo / Core | Mapa de necesidades / Needs map | `frontend/js/core/mapa-necesidades`, `backend/modules/necesidades` | En progreso / In progress (PR #18 abierto) |
| Núcleo / Core | Alertas oficiales (globales, GDACS) / Official alerts (global, GDACS) | `frontend/js/core/alertas-oficiales`, `backend/modules/alertas` | S1 hecho en `feature/alerts` / S1 done in `feature/alerts` (pendiente integración a dev / dev integration pending) |
| Núcleo / Core | Voluntariado y donaciones / Volunteering and donations | `frontend/js/core/voluntariado-donaciones`, `backend/modules/voluntariado`, `backend/modules/donaciones` | En progreso / In progress (frontend en dev; backend pendiente) |
| Siguiente / Next | Registro de personas / estoy bien / Person registry / I'm safe | `frontend/js/siguiente/registro-personas`, `backend/modules/personas` | En progreso / In progress (PR #20 abierto) |
| Siguiente / Next | Modo offline / Offline mode | `frontend/js/siguiente/modo-offline`, `backend/sync` | Pendiente (Sprint 2) / Pending (Sprint 2) |
| Futuro / Future | Red mesh / satélite / Mesh/satellite network | `infra/mesh-satelite` | Roadmap futuro / Future roadmap |
| Futuro / Future | Código abierto / Open source | `LICENSE`, `CONTRIBUTING.md` | Roadmap futuro / Future roadmap |

## Estado actual / Current status

- **Base común / Common base:** Completada. Índice, estilos, `apiClient.js`, arranque backend (`main.py`/`config.py`), BD y `seed.py`.
  Done. Index, styles, `apiClient.js`, backend bootstrap (`main.py`/`config.py`), DB and `seed.py`.
- **Alertas oficiales (G2) / Official alerts (G2):** Sprint 1 completado en `feature/alerts` (PR #19 mergeado). Pendiente integración a `dev` vía `juan/integrate-alerts-dev → feature/alerts` y `feature/alerts → dev`. Incluye `/api/alertas` con GDACS y fallback.
  Sprint 1 done in `feature/alerts` (PR #19 merged). Dev integration pending via `juan/integrate-alerts-dev → feature/alerts` and `feature/alerts → dev`. Includes `/api/alertas` with GDACS and fallback.
- **Mapa (G1) / Map (G1):** En progreso. PR #18 abierto y bloqueado (faltan GET/PATCH, quitar mock, centralizar en `necesidadesApi.js`).
  In progress. PR #18 open and blocked (missing GET/PATCH, remove mock, centralize in `necesidadesApi.js`).
- **Voluntariado/Donaciones (G3) / Volunteering/Donations (G3):** En progreso. Frontend en `dev`; backend pendiente.
  In progress. Frontend in `dev`; backend pending.
- **Personas/Offline (G4) / Persons/Offline (G4):** En progreso. PR #20 abierto (backend estoy-bien listo, 45 tests).
  In progress. PR #20 open (estoy-bien backend ready, 45 tests).
- **Kanban:** Los issues se crean automáticamente al mergear `feature/docs → dev` mediante `.github/workflows/setup-kanban.yml` (usa `GITHUB_TOKEN`). El tablero es un Project V2 personal del PM.
  Issues are auto-created when merging `feature/docs → dev` via `.github/workflows/setup-kanban.yml` (uses `GITHUB_TOKEN`). The board is a personal V2 Project owned by the PM.

## Equipos / Teams

La composición de los 4 equipos y el mapeo a los bloques del Kanban están en `docs/equipos.md`.

Team composition (4 teams) and the mapping to Kanban blocks are in `docs/equipos.md`.
