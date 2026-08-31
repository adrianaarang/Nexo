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
- `docs/equipos/grupo1-tareas.md` — reparto del Grupo 1 (Necesidades).
- `docs/equipos/grupo2-tareas.md` — guion de reunión y checklist del Grupo 2 (Alertas + activación).
- `docs/equipos/grupo3-tareas.md` — reparto del Grupo 3 (Ayudas: donación + voluntariado).
- `docs/equipos/grupo4-tareas.md` — reparto del Grupo 4 (Mapa + Interfaz principal).
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

| Prioridad | Módulo | Carpeta | Estado (2026-08-31) |
|---|---|---|---|
| Núcleo | Mapa de necesidades / Needs map — Necesidades (G1) | `frontend/js/core/mapa-necesidades` + `geocodificacion.js`, `backend/modules/necesidades` | En `dev` (MERGED #18, #22, #25, #56, #61) — rediseño 8 cats/2 estados + `direccion` + `services.py` + geocodificación (91a7647) |
| Núcleo | Alertas oficiales (globales, GDACS) / Official alerts — Alertas (G2) | `frontend/js/core/alertas-oficiales`, `backend/modules/alertas` | Sprint 1 (G2) listo en `feature/alerts` (G2-only tras revertir #30); PR G2 → dev pendiente |
| Núcleo | Voluntariado y donaciones / Volunteering and donations — Ayudas (G3) | `frontend/js/core/voluntariado-donaciones`, `backend/modules/voluntariado`, `backend/modules/donaciones` | En `dev` (MERGED #24, #27, #29); falta conectar UI donaciones al backend |
| Siguiente | Registro de personas / estoy bien / Person registry / I'm safe | `frontend/js/siguiente/registro-personas`, `backend/modules/personas` | En `dev` (MERGED #20); Sprint 1 |
| Siguiente | Modo offline / Offline mode | `frontend/js/siguiente/modo-offline`, `backend/sync` | Backend en `dev` (#21); falta UI offline |
| Futuro | Red mesh / satélite / Mesh/satellite network | `infra/mesh-satelite` | Roadmap futuro |
| Futuro | Código abierto / Open source | `LICENSE`, `CONTRIBUTING.md` | Roadmap futuro |

## Estado actual (2026-08-31 — `dev` en 91a7647)

- **Base común:** En `dev` (mergeado vía #53). `dev` arranca (init_db idempotente) y conecta (CORS + `apiClient`) — ver `docs/equipos.md`.
- **Necesidades (G1):** En `dev`. Rediseño mergeado (#56 + #61): 8 categorías/2 estados + `direccion` + geocodificación + `services.py` (91a7647).
- **Alertas oficiales (G2):** Sprint 1 (G2) completado en `feature/alerts` (G2-only tras revertir #30). Pendiente integración a `dev`.
- **Ayudas (G3):** En `dev`. Registro, disponibilidad y configuración mergeados (#24, #27, #29). Falta conectar `donaciones.js` al backend real.
- **Personas/Offline:** "Estoy bien" en `dev` (MERGED #20). Backend sync offline en `dev` (MERGED #21); falta UI offline.
- **Kanban:** En `dev` (merge #53). Tablero Sprint 2 regenerado con `scripts/setup-kanban.sh`; `feature/docs` ya mergeado — ver `docs/backlog.md` y `.github/workflows/setup-kanban.yml`.

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
- `docs/equipos/grupo1-tareas.md` — Group 1 (Necesidades) task split.
- `docs/equipos/grupo2-tareas.md` — Group 2 meeting script and checklist (Alertas + activación).
- `docs/equipos/grupo3-tareas.md` — Group 3 (Ayudas: donation + volunteering) task split.
- `docs/equipos/grupo4-tareas.md` — Group 4 (Mapa + Interfaz principal) task split.
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

| Priority | Module | Folder | Status (2026-08-31) |
|---|---|---|---|
| Core | Needs map — Necesidades (G1) | `frontend/js/core/mapa-necesidades` + `geocodificacion.js`, `backend/modules/necesidades` | In `dev` (MERGED #18, #22, #25, #56, #61) — redesign 8 cats/2 states + `direccion` + `services.py` (91a7647) |
| Core | Official alerts — Alertas (G2) | `frontend/js/core/alertas-oficiales`, `backend/modules/alertas` | S1 (G2) done in `feature/alerts` (G2-only after revert); G2 PR → dev pending |
| Core | Volunteering and donations — Ayudas (G3) | `frontend/js/core/voluntariado-donaciones`, `backend/modules/voluntariado`, `backend/modules/donaciones` | In `dev` (MERGED #24, #27, #29); UI donations not yet wired |
| Next | Person registry / I'm safe | `frontend/js/siguiente/registro-personas`, `backend/modules/personas` | In `dev` (MERGED #20); Sprint 1 |
| Next | Offline mode | `frontend/js/siguiente/modo-offline`, `backend/sync` | Backend in `dev` (#21); offline UI pending |
| Future | Mesh/satellite network | `infra/mesh-satelite` | Future roadmap |
| Future | Open source | `LICENSE`, `CONTRIBUTING.md` | Future roadmap |

## Current status (2026-08-31 — `dev` at 91a7647)

- **Common base:** In `dev` (merged via #53). `dev` boots (init_db idempotent) and connects (CORS + `apiClient`).
- **Needs (G1):** In `dev`. Redesign merged (#56 + #61): 8 cats/2 states + `direccion` + geocoding + `services.py` (91a7647).
- **Official alerts (G2):** S1 (G2) completed in `feature/alerts` (G2-only after revert). Pending `dev` integration.
- **Aid (G3):** In `dev`. Registration, availability, config merged (#24, #27, #29). UI `donaciones.js` pending.
- **Persons/Offline:** "I'm safe" in `dev` (MERGED #20). Sync backend in `dev` (MERGED #21); offline UI pending.
- **Kanban:** In `dev` (merged #53). Sprint 2 board regenerated with `scripts/setup-kanban.sh`; `feature/docs` already merged.

## Teams

Team composition (4 teams) and the mapping to Kanban blocks are in `docs/equipos.md`.

</details>
