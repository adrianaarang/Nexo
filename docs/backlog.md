# Backlog de NEXO

> Mantenido por el Product Manager (Juan). Última actualización: 2026-08-26 (post-merges de Sprint 1; PR #30 con conflicto resuelto).
> Referencia de prioridades: `docs/manifiesto.md` y `docs/roadmap.md`.

## Estado por módulo

| Módulo | Prioridad | Rama(s) | PR | Dueño | Estado |
|--------|-----------|---------|----|-------|--------|
| Alertas oficiales | Núcleo (MVP) | `feature/alerts` | #30 **ABIERTO** (mergeable) | Grupo 2 (Juan, capitán) | Backend + pantalla + tests en verde (feature/alerts). PR #30 a `dev` abierto, 0/2 aprobaciones; conflicto con `dev` resuelto el 26/08. |
| Mapa de necesidades | Núcleo (MVP) | `dev` | #18 **MERGED** | Grupo 1 + elenadiaz1 | En `dev`: backend + frontend conectados (datos reales). |
| Voluntariado y donaciones | Núcleo (MVP) | `dev` | #24, #27, #29 **MERGED** | Grupo 3 | En `dev`: registro + disponibilidad + config/soporte. Falta conectar `donaciones.js` al backend real. |
| Registro de personas / "estoy bien" | Siguiente | `dev` | #20 **MERGED** | Grupo 4 | En `dev`: backend "estoy bien" (45 tests). **Sprint 1**. |
| Modo offline (PWA) | Siguiente | `dev` | #21 **MERGED** (backend) | Grupo 4 | Backend de sincronización en `dev`; falta UI offline en frontend. |
| Documentación y gobernanza | Transversal | `feature/docs` | por abrir | PM (Juan) | README bilingüe, `equipos.md`, `equipos/grupo*-tareas.md`, `.github/workflows/setup-kanban.yml` en `feature/docs` (pendiente merge a `dev`). |

## PRs (2026-08-26)

| PR | Título | Estado |
|----|--------|--------|
| #18 | Feature/form cards (mapa E2E) | **MERGED** a `dev` |
| #19 / #26 / #28 | Alertas backend / fixes CORS+apiClient / refactor resiliente + stub PC | **MERGED** a `feature/alerts` |
| #20 | feat(personas): add estoy bien backend | **MERGED** a `dev` |
| #21 | feat(sync): offline synchronization backend (G4) | **MERGED** a `dev` |
| #22 | Integración necesidadesApi.js | **MERGED** a `dev` |
| #23 | fix(api): validation error format | **MERGED** a `dev` |
| #24 | feat(voluntariado): volunteer module | **MERGED** a `dev` |
| #25 | Añadir kanban del Equipo 1 | **MERGED** a `dev` |
| #27 | chore(voluntariado): config and support | **MERGED** a `dev` |
| #29 | feat(voluntariado): volunteer registration | **MERGED** a `dev` |
| #30 | feat(alertas): integrate alerts module into dev (Sprint 1) | **ABIERTO**, mergeable (conflicto resuelto), 0/2 aprobaciones |

## Tablero / Kanban

Los issues (epics por bloque/equipo) se crean **automáticamente** al mergear `feature/docs → dev` mediante `.github/workflows/setup-kanban.yml` (usa `GITHUB_TOKEN`, sin permisos extra). `Base común` y `Equipo 2` se cierran al crearse; el resto se cierra solo al mergear sus PR de integración si incluyen `Closes #<num>`. El tablero visual es un Project V2 personal del PM (agrupado por Label = equipo, columnas por Status). Composición de equipos en `docs/equipos.md`.

> Nota: el tablero aún no existe porque `feature/docs` no se ha mergeado a `dev`.

## Objetivos MVP (de `docs/manifiesto.md`)
- [ ] O1 Alertas GDACS con filtros y estados (núcleo del Grupo 2) — feature/alerts listo, falta #30 a dev
- [ ] O2 Mapa de necesidades end-to-end — en dev
- [ ] O3 Voluntariado/donaciones end-to-end — backend en dev; falta UI donaciones
- [ ] O4 E2E completo (frontend→API→BD) con CI verde — depende de #30 + CI en dev
- [ ] O5 PWA instalable con detección de conexión — offline backend en dev

## Pendientes de gobernanza (PM)
- [ ] Activar CI también en `dev` (hoy solo corre en `main`) — responsabilidad de Adriana.
- [ ] Votar la convención bilingüe (manifiesto la dejó "pendiente de votación").
- [ ] Mergear `feature/docs → dev` (crea el tablero Kanban y deja README bilingüe oficial).
- [ ] Cerrar la UI offline en el frontend (backend ya en `dev` vía #21).
- [ ] Limpiar `feature/alerts-vanessa` (rama duplicada de alertas).
- [ ] Preparar Demo Day (narrativa alerta→mapa→necesidad→recurso→resolución).
- [x] Decidir herramienta de backlog: Trello — decidido.

## Abierto (por decidir)
- Zonas/celdas del mapa aún no definidas.
- Alcance exacto del modo offline (decisión abierta).
- Estrategia de despliegue (solo local hoy; CI sin despliegue).

## Riesgos
- **Alertas (#30):** único módulo núcleo fuera de `dev`; conseguir 2 aprobaciones (JCRbit, adrianaarang, vanessa, luis, joel). Conflicto con `dev` ya resuelto (merge de `dev` into `feature/alerts`, commit `da648ba`).
- **CI:** solo en `main`; `dev` sin protección de CI verde.
- **Rama duplicada:** `feature/alerts-vanessa` se solapa con `feature/alerts`.
