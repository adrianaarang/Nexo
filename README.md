# Nexo — Conectados para ayudarnos

> 🇪🇸 Español más abajo. 🇬🇧 Traducción completa al inglés en la sección plegable al final.

App comunitaria de respuesta a emergencias y desastres naturales: mapa de necesidades en tiempo real, alertas oficiales, voluntariado y donaciones. El registro de personas y el modo sin conexión son las siguientes prioridades. La red mesh/satélite y el código abierto quedan como roadmap futuro.

Alcance decidido por votación de equipo — ver `docs/decisiones-encuesta.md` y `docs/roadmap.md`.

## ¿Qué es Nexo? (Visión de producto)

Nexo es una aplicación comunitaria de respuesta ante emergencias y desastres naturales. Ante un terremoto, una inundación o un incendio, la información está fragmentada: los afectados no saben dónde pedir ayuda, los voluntarios no ven dónde se les necesita y las autoridades no tienen un canal ciudadano en tiempo real. Nexo reúne esas tres miradas en una sola pantalla:

- un **mapa de necesidades** vivo, donde cualquiera publica y ve qué falta en cada zona;
- **alertas oficiales** verificadas (GDACS) con filtros por país y tipo;
- un módulo de **voluntariado y donaciones** para coordinar apoyo;
- un **registro de personas ("estoy bien")** que cierra la incertidumbre sobre familiares y vecinos.

El objetivo es reducir el tiempo entre "algo pasa" y "alguien recibe ayuda".

## Propuesta de valor y modelo de impacto (Negocio)

Nexo no es un producto comercial: es una solución cívica, sin ánimo de lucro y de origen académico. Su "modelo de negocio" es el impacto:

- **Para afectados:** visibilidad y un canal para pedir ayuda concreta (agua, refugio, transporte) en su zona.
- **Para voluntarios y donantes:** un mapa donde ver necesidades reales y coordinar apoyo, evitando la duplicación de esfuerzos.
- **Para ONG y protección civil:** un canal ciudadano de datos en tiempo real para priorizar recursos.
- **Sostenibilidad:** proyecto académico con licencia MIT provisional; el código abierto y la red mesh/satélite son el horizonte para que cualquier comunidad lo despliegue sin coste.

## Estructura (Técnico)

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
- `docs/equipos/grupo3-tareas.md` — reparto del Grupo 3 (Voluntariado y Donaciones).
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

| Prioridad | Módulo | Carpeta | Estado (2026-08-26) |
|---|---|---|---|
| Núcleo | Mapa de necesidades / Needs map | `frontend/js/core/mapa-necesidades`, `backend/modules/necesidades` | En `dev` (MERGED #18, #22, #25) |
| Núcleo | Alertas oficiales (globales, GDACS) / Official alerts (global, GDACS) | `frontend/js/core/alertas-oficiales`, `backend/modules/alertas` | Sprint 1 listo en `feature/alerts`; PR #30 abierto y mergeable |
| Núcleo | Voluntariado y donaciones / Volunteering and donations | `frontend/js/core/voluntariado-donaciones`, `backend/modules/voluntariado`, `backend/modules/donaciones` | En `dev` (MERGED #24, #27, #29); falta conectar UI donaciones al backend |
| Siguiente | Registro de personas / estoy bien / Person registry / I'm safe | `frontend/js/siguiente/registro-personas`, `backend/modules/personas` | En `dev` (MERGED #20); Sprint 1 |
| Siguiente | Modo offline / Offline mode | `frontend/js/siguiente/modo-offline`, `backend/sync` | Backend en `dev` (#21); falta UI offline |
| Futuro | Red mesh / satélite / Mesh/satellite network | `infra/mesh-satelite` | Roadmap futuro |
| Futuro | Código abierto / Open source | `LICENSE`, `CONTRIBUTING.md` | Roadmap futuro |

## Estado actual

- **Base común:** Completada. Índice, estilos, `apiClient.js`, arranque backend (`main.py`/`config.py`), BD y `seed.py`.
- **Alertas oficiales (G2):** Sprint 1 completado y verificado en `feature/alerts` (API `/api/alertas` con GDACS + fallback, pantalla y tests en verde). Pendiente integración a `dev` (PR #30, abierto y mergeable tras resolver conflicto con `dev`).
- **Mapa (G1):** En `dev`. Backend + frontend conectados con datos reales (MERGED #18, #22, #25).
- **Voluntariado/Donaciones (G3):** En `dev`. Registro, disponibilidad y configuración mergeados (#24, #27, #29). Falta conectar `donaciones.js` al backend real.
- **Personas/Offline (G4):** "Estoy bien" en `dev` (MERGED #20, 45 tests). Backend de sincronización offline en `dev` (MERGED #21); falta la UI offline en el frontend.
- **Kanban:** Los issues se crean automáticamente al mergear `feature/docs → dev` mediante `.github/workflows/setup-kanban.yml` (usa `GITHUB_TOKEN`). El tablero es un Project V2 personal del PM.

## Equipos

La composición de los 4 equipos y el mapeo a los bloques del Kanban están en `docs/equipos.md`.

---

<details>
<summary>🇬🇧 English version</summary>

# Nexo — Connected to help each other

Community app for emergency and natural-disaster response: real-time needs map, official alerts, volunteering and donations. Person registry and offline mode are the next priorities. Mesh/satellite network and open source remain future roadmap.

Scope decided by team vote — see `docs/decisiones-encuesta.md` and `docs/roadmap.md`.

## What is Nexo? (Product vision)

Nexo is a community app for responding to emergencies and natural disasters. During an earthquake, flood or fire, information is fragmented: those affected don't know where to ask for help, volunteers can't see where they are needed, and authorities lack a real-time citizen channel. Nexo brings those three views together on a single screen:

- a live **needs map**, where anyone posts and sees what is missing in each area;
- verified **official alerts** (GDACS) with filters by country and type;
- a **volunteering and donations** module to coordinate support;
- a **person registry ("I'm safe")** that closes the uncertainty about family and neighbours.

The goal is to shorten the time between "something happens" and "someone gets help".

## Value proposition and impact model (Business)

Nexo is not a commercial product: it is a civic, non-profit, academically originated solution. Its "business model" is impact:

- **For those affected:** visibility and a channel to request concrete help (water, shelter, transport) in their area.
- **For volunteers and donors:** a map to see real needs and coordinate support, avoiding duplicated effort.
- **For NGOs and civil protection:** a real-time citizen data channel to prioritise resources.
- **Sustainability:** an academic project under a provisional MIT licence; open source and the mesh/satellite network are the horizon so any community can deploy it at no cost.

## Structure (Technical)

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
- `docs/equipos/grupo3-tareas.md` — Group 3 (Volunteering and donations) task split.
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

| Priority | Module | Folder | Status (2026-08-26) |
|---|---|---|---|
| Core | Needs map | `frontend/js/core/mapa-necesidades`, `backend/modules/necesidades` | In `dev` (MERGED #18, #22, #25) |
| Core | Official alerts (global, GDACS) | `frontend/js/core/alertas-oficiales`, `backend/modules/alertas` | S1 done in `feature/alerts`; PR #30 open and mergeable |
| Core | Volunteering and donations | `frontend/js/core/voluntariado-donaciones`, `backend/modules/voluntariado`, `backend/modules/donaciones` | In `dev` (MERGED #24, #27, #29); UI donations not yet wired to backend |
| Next | Person registry / I'm safe | `frontend/js/siguiente/registro-personas`, `backend/modules/personas` | In `dev` (MERGED #20); Sprint 1 |
| Next | Offline mode | `frontend/js/siguiente/modo-offline`, `backend/sync` | Backend in `dev` (#21); offline UI pending |
| Future | Mesh/satellite network | `infra/mesh-satelite` | Future roadmap |
| Future | Open source | `LICENSE`, `CONTRIBUTING.md` | Future roadmap |

## Current status

- **Common base:** Done. Index, styles, `apiClient.js`, backend bootstrap (`main.py`/`config.py`), DB and `seed.py`.
- **Official alerts (G2):** Sprint 1 completed and verified in `feature/alerts` (API `/api/alertas` with GDACS + fallback, screen and tests green). Dev integration pending (PR #30, open and mergeable after resolving the conflict with `dev`).
- **Map (G1):** In `dev`. Backend + frontend connected with real data (MERGED #18, #22, #25).
- **Volunteering/Donations (G3):** In `dev`. Registration, availability and configuration merged (#24, #27, #29). UI `donaciones.js` still needs to be wired to the real backend.
- **Persons/Offline (G4):** "I'm safe" in `dev` (MERGED #20, 45 tests). Offline sync backend in `dev` (MERGED #21); offline UI still pending.
- **Kanban:** Issues are auto-created when merging `feature/docs → dev` via `.github/workflows/setup-kanban.yml` (uses `GITHUB_TOKEN`). The board is a personal V2 Project owned by the PM.

## Teams

Team composition (4 teams) and the mapping to Kanban blocks are in `docs/equipos.md`.

</details>
