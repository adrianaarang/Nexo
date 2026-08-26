# Backlog de NEXO

> Mantenido por el Product Manager (Juan). Última actualización: 2026-08-26 (Sprint 1 integrado en `dev`; pendiente merge de #46 para el workflow de Kanban en CI).
> Referencia de prioridades: `docs/manifiesto.md` y `docs/roadmap.md`.

## Estado por módulo

| Módulo | Prioridad | Rama(s) | PR | Dueño | Estado |
|--------|-----------|---------|----|-------|--------|
| Alertas oficiales | Núcleo (MVP) | `dev` | #34 **MERGED** (era #56) | Grupo 2 (Juan, capitán) | En `dev`: backend GDACS + fallback, filtros país ES→EN, frontend `alertas.html`, tests verdes. G2-only tras revertir #30 con #32. |
| Mapa de necesidades | Núcleo (MVP) | `dev` | #18, #22, #25, #37 **MERGED** | Grupo 1 + elenadiaz1 | En `dev`: backend + frontend conectados (datos reales); #37 corrige el flujo de estado abierta→en_proceso→cubierta. |
| Voluntariado y donaciones | Núcleo (MVP) | `dev` | #24, #27, #29 **MERGED** | Grupo 3 | En `dev`: registro + disponibilidad + config/soporte. Falta conectar `donaciones.js` al backend real. |
| Registro de personas / "estoy bien" | Siguiente | `dev` | #20 **MERGED** | Grupo 4 | En `dev`: backend "estoy bien" (45 tests). **Sprint 1**. |
| Modo offline (PWA) | Siguiente | `dev` | #21 **MERGED** (backend) | Grupo 4 | Backend de sincronización en `dev`; falta UI offline en el frontend. |
| Documentación y gobernanza | Transversal | `dev` | #36 **MERGED** (era `feature/docs`) | PM (Juan) | README bilingüe, `equipos.md`, `equipos/grupo*-tareas.md`, `.github/workflows/setup-kanban.yml` en `dev`. |
| Kanban (automatización) | Transversal | `fix/setup-kanban` | #46 **ABIERTO** | PM (Juan) | Corrige `scripts/setup-kanban.sh` para que el workflow corra en CI; pendiente de merge. |

## PRs

### Mergeados a `dev` (Sprint 1)

| PR | Título | Notas |
|----|--------|-------|
| #18 | Feature/form cards (mapa E2E) | |
| #19 / #26 / #28 | Alertas backend / fixes CORS+apiClient / refactor resiliente + stub PC | en `feature/alerts` |
| #20 | feat(personas): add estoy bien backend | |
| #21 | feat(sync): offline synchronization backend (G4) | |
| #22 | Integración necesidadesApi.js | |
| #23 | fix(api): validation error format | |
| #24 | feat(voluntariado): volunteer module | |
| #25 | Añadir kanban del Equipo 1 | |
| #27 | chore(voluntariado): config and support | |
| #29 | feat(voluntariado): volunteer registration | |
| #30 | feat(alertas): integrate alerts module into dev (Sprint 1) | **REVERTIDO** con #32 |
| #32 | Revert "feat(alertas): integrate alerts module into dev" | |
| #34 | feat(alertas): G2 official alerts module (GDACS) — Sprint 1 | `feature/alerts` → `dev` (G2-only) |
| #35 | fix(base-comun): init_db, CORS and apiClient to boot dev | `fix/base-comun` → `dev` |
| #36 | docs: general project status and Sprint 1 traceability | `feature/docs` → `dev` |
| #37 | fix(mapa-necesidades): flujo de estado y contrato español | `fix-mapa-necesidades` → `dev` |
| #38 | actualizar-kanban: mejoras de punto en el mapa y 4 mejoras con IA | → `dev` |

### Abiertos / en curso

| PR / Rama | Título | Estado |
|-----------|--------|--------|
| #46 | fix(ci): setup-kanban compatible with older gh CLI | **ABIERTO** (`fix/setup-kanban` → `dev`) — corrige el workflow de Kanban |
| #33 (feature/personas/isabela) | sync personas + offline | **ABIERTO**, backend-tests en rojo; en revisión |
| feature/donaciones-grupo3 | Voluntariado/donaciones G3 | en curso (falta UI donaciones) |
| feature/modo-offline/abdur | Modo offline (Abdur) | en curso (falta UI offline) |
| feature/alerts-vanessa | Alertas (rama duplicada) | pendiente de limpieza |

## Tablero / Kanban

Los issues (epics por bloque/equipo) se crean automáticamente al ejecutar `.github/workflows/setup-kanban.yml` (usa `GITHUB_TOKEN`). `Base común` (#40) y `Equipo 2` (#42) se cierran al crearse; el resto se cierra al mergear sus PR de integración si incluyen `Closes #<num>`. El tablero visual es un Project V2 personal del PM (agrupado por Label = equipo, columnas por Status). Composición de equipos en `docs/equipos.md`.

Issues creados (2026-08-25):

| # | Título | Label | Estado |
|---|--------|-------|--------|
| #40 | Base comun - revision previa al reparto | base-comun, kanban | **CERRADO** |
| #41 | Equipo 1 - Mapa de necesidades | equipo-1, kanban | Abierto |
| #42 | Equipo 2 - Alertas oficiales | equipo-2, kanban | **CERRADO** |
| #43 | Equipo 3 - Voluntariado y donaciones | equipo-3, kanban | Abierto |
| #44 | Equipo 4 - Personas y modo offline | equipo-4, kanban | Abierto |
| #45 | Futuro - Resilience OS | futuro, kanban | Abierto |

> El workflow se dispara con `on: push` a `dev` y `workflow_dispatch`. Tras mergear #46 correrá de forma idempotente (omite los issues ya existentes).

## Objetivos MVP (de `docs/manifiesto.md`)

- [x] O1 Alertas GDACS con filtros y estados — en `dev` (#34)
- [x] O2 Mapa de necesidades end-to-end — en `dev`
- [ ] O3 Voluntariado/donaciones end-to-end — backend en `dev`; falta UI donaciones
- [ ] O4 E2E completo (frontend→API→BD) con CI verde — depende de UI donaciones/offline + CI en `dev`
- [ ] O5 PWA instalable con detección de conexión — offline backend en `dev`; falta UI offline

## Trazabilidad Sprint 1 (entrega)

Resumen del estado de los 4 equipos y la base común a fecha 2026-08-26, tras integrar #34, #35 y #36 en `dev`.

| Equipo / Base | Módulo | Rama | PR a `dev` | Estado |
|---------------|--------|------|-----------|--------|
| Base común | Arranque backend + CORS + apiClient | `dev` | #35 **MERGED** | En `dev`: arranca y conecta |
| Grupo 1 | Mapa de necesidades | `dev` | #18, #22, #25, #37 **MERGED** | En `dev`, datos reales |
| Grupo 2 | Alertas oficiales (GDACS) | `dev` | #34 **MERGED** | G2-only, filtro país ES→EN, tests verdes |
| Grupo 3 | Voluntariado y donaciones | `dev` | #24, #27, #29 **MERGED** | En `dev`; falta UI donaciones |
| Grupo 4 | Personas / "estoy bien" + offline | `dev` | #20, #21 **MERGED** | En `dev`; falta UI offline |
| PM / Docs | Estado y gobernanza | `dev` | #36 **MERGED** | README bilingüe + Kanban en `dev` |

**Revisiones:** #46 (setup-kanban) abierto y pendiente de merge para activar el workflow en CI. #33 (personas/Isabela) en revisión con backend-tests en rojo.

## Pendientes de gobernanza (PM)

- [ ] Mergear #46 (`fix/setup-kanban` → `dev`) para que el workflow de Kanban corra en CI.
- [ ] Activar CI también en `dev` (hoy solo corre en `main`).
- [ ] Cerrar la UI offline en el frontend (backend ya en `dev` vía #21).
- [ ] Conectar `donaciones.js` al backend real (G3).
- [ ] Cerrar reparto de tareas del Grupo 4 (`docs/equipos/grupo4-tareas.md`).
- [ ] Limpiar `feature/alerts-vanessa` (rama duplicada de alertas).
- [x] Decidir herramienta de backlog: Trello — decidido.
- [x] Votar la convención bilingüe (README bilingüe oficial en `dev`).

## Abierto (por decidir)

- Zonas/celdas del mapa aún no definidas.
- Alcance exacto del modo offline (decisión abierta).
- Estrategia de despliegue (solo local hoy; CI sin despliegue).

## Riesgos

- **UI donaciones/offline:** módulos con backend en `dev` pero falta la capa frontend; son el trabajo del Sprint 2.
- **CI:** solo en `main`; `dev` sin protección de CI verde (pendiente activar).
- **Rama duplicada:** `feature/alerts-vanessa` se solapa con `feature/alerts`.
