# Nexo — Conectados para ayudarnos

> 🇪🇸 Español más abajo. 🇬🇧 Traducción completa al inglés en la sección plegable al final.

App comunitaria de respuesta a emergencias y desastres naturales: mapa de necesidades en tiempo real, alertas oficiales, voluntariado y donaciones. El registro de personas y el modo sin conexión son las siguientes prioridades. La red mesh/satélite y el código abierto quedan como roadmap futuro.

Alcance decidido por votación de equipo — ver `docs/decisiones-encuesta.md` y `docs/roadmap.md`.

## Estructura

- `frontend/` — HTML, CSS y JS (PWA).
- `backend/` — API en Python (FastAPI).
- `docs/` — decisiones de producto, arquitectura y privacidad.
- `infra/` — notas de infraestructura futura (red mesh/satélite).

## Documentación de gobernanza

- `docs/manifiesto.md` — visión, principios, objetivos MVP y organización del proyecto.
- `docs/convenciones.md` — reglas de equipo (ramas, commits, PRs, ADRs, propiedad de archivos).
- `docs/reparto-trabajo.md` — reparto en 4 equipos y base común.
- `docs/formas-de-trabajo.md` — acuerdos de equipo (Trello, estilos, alcance, PRs).
- `docs/roles-y-tareas.md` — roles y división de tareas por grupo (cada SM completa su sección).
- `docs/faq.md` — preguntas frecuentes y decisiones curadas (Grupo 2 y Grupo 4).
- `docs/backlog.md` — estado por módulo y pendientes de gobernanza (mantenido por el PM).
- `docs/equipos.md` — composición de los 4 equipos y mapeo a bloques del Kanban.
- `docs/equipos/grupo1-tareas.md` — reparto del Grupo 1 (Mapa/Necesidades).
- `docs/equipos/grupo2-tareas.md` — guion de reunión y checklist del Grupo 2.
- `estructura/` — guías de estructura de archivos (`estructuranexo.md`, `estructuranexoexplicada.md`).

## Cómo arrancar

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python db/seed.py               # datos de ejemplo
uvicorn main:app --reload --port 8000
```

La API queda disponible en `http://localhost:8000`. Documentación automática en `http://localhost:8000/docs`.

### Frontend

No necesita build. Sirve la carpeta `frontend/` con cualquier servidor estático, por ejemplo:

```bash
cd frontend
python -m http.server 5500
```

Abre `http://localhost:5500`. El frontend espera la API en `http://localhost:8000` (configurable en `frontend/js/shared/apiClient.js`).

## Módulos

| Prioridad | Módulo | Carpeta | Estado |
|---|---|---|---|
| Núcleo | Mapa de necesidades / Needs map | `frontend/js/core/mapa-necesidades`, `backend/modules/necesidades` | En progreso (PR #18 abierto) |
| Núcleo | Alertas oficiales (globales, GDACS) / Official alerts (global, GDACS) | `frontend/js/core/alertas-oficiales`, `backend/modules/alertas` | S1 hecho en `feature/alerts` (pendiente integración a `dev`) |
| Núcleo | Voluntariado y donaciones / Volunteering and donations | `frontend/js/core/voluntariado-donaciones`, `backend/modules/voluntariado`, `backend/modules/donaciones` | En progreso (frontend en dev; backend pendiente) |
| Siguiente | Registro de personas / estoy bien / Person registry / I'm safe | `frontend/js/siguiente/registro-personas`, `backend/modules/personas` | En progreso (PR #20 abierto) |
| Siguiente | Modo offline / Offline mode | `frontend/js/siguiente/modo-offline`, `backend/sync` | Pendiente (Sprint 2) |
| Futuro | Red mesh / satélite / Mesh/satellite network | `infra/mesh-satelite` | Roadmap futuro |
| Futuro | Código abierto / Open source | `LICENSE`, `CONTRIBUTING.md` | Roadmap futuro |

## Estado actual

- **Base común:** Completada. Índice, estilos, `apiClient.js`, arranque backend (`main.py`/`config.py`), BD y `seed.py`.
- **Alertas oficiales (G2):** Sprint 1 completado y verificado en `feature/alerts` (API `/api/alertas` con GDACS + fallback, pantalla y tests en verde). Pendiente integración a `dev` (PR `feature/alerts` → `dev`).
- **Mapa (G1):** En progreso. PR #18 abierto y bloqueado (faltan GET/PATCH, quitar mock, centralizar en `necesidadesApi.js`).
- **Voluntariado/Donaciones (G3):** En progreso. Frontend en `dev`; backend pendiente. PR #27 (config/soporte) en revisión.
- **Personas/Offline (G4):** En progreso. PR #20 abierto (backend estoy-bien listo, 45 tests).
- **Kanban:** Los issues se crean automáticamente al mergear `feature/docs → dev` mediante `.github/workflows/setup-kanban.yml` (usa `GITHUB_TOKEN`). El tablero es un Project V2 personal del PM.

## Equipos

La composición de los 4 equipos y el mapeo a los bloques del Kanban están en `docs/equipos.md`.

---

<details>
<summary>🇬🇧 English version</summary>

# Nexo — Connected to help each other

Community app for emergency and natural-disaster response: real-time needs map, official alerts, volunteering and donations. Person registry and offline mode are the next priorities. Mesh/satellite network and open source remain future roadmap.

Scope decided by team vote — see `docs/decisiones-encuesta.md` and `docs/roadmap.md`.

## Structure

- `frontend/` — HTML, CSS and JS (PWA).
- `backend/` — Python API (FastAPI).
- `docs/` — product decisions, architecture and privacy.
- `infra/` — future infrastructure notes (mesh/satellite network).

## Governance documentation

- `docs/manifiesto.md` — vision, principles, MVP objectives and project organization.
- `docs/convenciones.md` — team rules (branches, commits, PRs, ADRs, file ownership).
- `docs/reparto-trabajo.md` — split into 4 teams and common base.
- `docs/formas-de-trabajo.md` — team agreements (Trello, styles, scope, PRs).
- `docs/roles-y-tareas.md` — roles and task split per group (each SM fills their section).
- `docs/faq.md` — FAQ and curated decisions (Group 2 and Group 4).
- `docs/backlog.md` — per-module status and governance pending items (maintained by PM).
- `docs/equipos.md` — composition of the 4 teams and mapping to Kanban blocks.
- `docs/equipos/grupo1-tareas.md` — Group 1 (Needs Map) task split.
- `docs/equipos/grupo2-tareas.md` — Group 2 meeting script and checklist.
- `estructura/` — file structure guides (`estructuranexo.md`, `estructuranexoexplicada.md`).

## How to run

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python db/seed.py
uvicorn main:app --reload --port 8000
```

The API is available at `http://localhost:8000`. Auto docs at `http://localhost:8000/docs`.

### Frontend

No build needed. Serve the `frontend/` folder with any static server, e.g.:

```bash
cd frontend
python -m http.server 5500
```

Open `http://localhost:5500`. The frontend expects the API at `http://localhost:8000` (configurable in `frontend/js/shared/apiClient.js`).

## Modules

| Priority | Module | Folder | Status |
|---|---|---|---|
| Core | Needs map | `frontend/js/core/mapa-necesidades`, `backend/modules/necesidades` | In progress (PR #18 open) |
| Core | Official alerts (global, GDACS) | `frontend/js/core/alertas-oficiales`, `backend/modules/alertas` | S1 done in `feature/alerts` (dev integration pending) |
| Core | Volunteering and donations | `frontend/js/core/voluntariado-donaciones`, `backend/modules/voluntariado`, `backend/modules/donaciones` | In progress (frontend in dev; backend pending) |
| Next | Person registry / I'm safe | `frontend/js/siguiente/registro-personas`, `backend/modules/personas` | In progress (PR #20 open) |
| Next | Offline mode | `frontend/js/siguiente/modo-offline`, `backend/sync` | Pending (Sprint 2) |
| Future | Mesh/satellite network | `infra/mesh-satelite` | Future roadmap |
| Future | Open source | `LICENSE`, `CONTRIBUTING.md` | Future roadmap |

## Current status

- **Common base:** Done. Index, styles, `apiClient.js`, backend bootstrap (`main.py`/`config.py`), DB and `seed.py`.
- **Official alerts (G2):** Sprint 1 completed and verified in `feature/alerts` (API `/api/alertas` with GDACS + fallback, screen and tests green). Dev integration pending (PR `feature/alerts` → `dev`).
- **Map (G1):** In progress. PR #18 open and blocked (missing GET/PATCH, remove mock, centralize in `necesidadesApi.js`).
- **Volunteering/Donations (G3):** In progress. Frontend in `dev`; backend pending. PR #27 (config/support) under review.
- **Persons/Offline (G4):** In progress. PR #20 open (estoy-bien backend ready, 45 tests).
- **Kanban:** Issues are auto-created when merging `feature/docs → dev` via `.github/workflows/setup-kanban.yml` (uses `GITHUB_TOKEN`). The board is a personal V2 Project owned by the PM.

## Teams

Team composition (4 teams) and the mapping to Kanban blocks are in `docs/equipos.md`.

</details>
