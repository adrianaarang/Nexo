# Backlog de NEXO

> Mantenido por el Product Manager (Juan). Última actualización: 2026-08-25 (Sprint 1: #30 revertido con #32; abiertos #56 feature/alerts, fix/base-comun y feature/docs).
> Referencia de prioridades: `docs/manifiesto.md` y `docs/roadmap.md`.

## Estado por módulo

| Módulo | Prioridad | Rama(s) | PR | Dueño | Estado |
|--------|-----------|---------|----|-------|--------|
| Alertas oficiales | Núcleo (MVP) | `feature/alerts`, `fix/base-comun` | #56 **ABIERTO** (feature/alerts→dev, G2-only) · `fix/base-comun`→dev **ABIERTO** | Grupo 2 (Juan, capitán) | Backend + pantalla + tests en verde (feature/alerts, G2-only tras revertir #30 con #32). Base común separada en `fix/base-comun` (dev no arranca tras revertir #30). |
| Mapa de necesidades | Núcleo (MVP) | `dev` | #18 **MERGED** | Grupo 1 + elenadiaz1 | En `dev`: backend + frontend conectados (datos reales). |
| Voluntariado y donaciones | Núcleo (MVP) | `dev` | #24, #27, #29 **MERGED** | Grupo 3 | En `dev`: registro + disponibilidad + config/soporte. Falta conectar `donaciones.js` al backend real. |
| Registro de personas / "estoy bien" | Siguiente | `dev` | #20 **MERGED** | Grupo 4 | En `dev`: backend "estoy bien" (45 tests). **Sprint 1**. |
| Modo offline (PWA) | Siguiente | `dev` | #21 **MERGED** (backend) | Grupo 4 | Backend de sincronización en `dev`; falta UI offline en frontend. |
| Documentación y gobernanza | Transversal | `feature/docs` | **ABIERTO** (feature/docs→dev) | PM (Juan) | README bilingüe, `equipos.md`, `equipos/grupo*-tareas.md`, `.github/workflows/setup-kanban.yml` en `feature/docs` (pendiente merge a `dev`). |

## PRs (2026-08-25)

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
| #30 | feat(alertas): integrate alerts module into dev (Sprint 1) | **REVERTIDO** con #32 (dev vuelve a pre-alertas) |
| #32 | Revert "feat(alertas): integrate alerts module into dev" | **MERGED** a `dev` |
| #56 | feat(alertas): G2 official alerts module (GDACS) — Sprint 1 | **ABIERTO** (feature/alerts→dev, G2-only) |
| `fix/base-comun`→dev | fix(base-comun): init_db, CORS and apiClient to boot dev | **ABIERTO** (base común; dev roto tras #30) |
| `feature/docs`→dev | docs: general project status and Sprint 1 traceability | **ABIERTO** (crea tablero Kanban) |

## Tablero / Kanban

Los issues (epics por bloque/equipo) se crean **automáticamente** al mergear `feature/docs → dev` mediante `.github/workflows/setup-kanban.yml` (usa `GITHUB_TOKEN`, sin permisos extra). `Base común` y `Equipo 2` se cierran al crearse; el resto se cierra solo al mergear sus PR de integración si incluyen `Closes #<num>`. El tablero visual es un Project V2 personal del PM (agrupado por Label = equipo, columnas por Status). Composición de equipos en `docs/equipos.md`.

> Nota: el tablero aún no existe porque `feature/docs` no se ha mergeado a `dev`.

## Objetivos MVP (de `docs/manifiesto.md`)
- [ ] O1 Alertas GDACS con filtros y estados (núcleo del Grupo 2) — feature/alerts (G2) listo, falta PR #56 a dev; base común en fix/base-comun
- [ ] O2 Mapa de necesidades end-to-end — en dev
- [ ] O3 Voluntariado/donaciones end-to-end — backend en dev; falta UI donaciones
- [ ] O4 E2E completo (frontend→API→BD) con CI verde — depende de #56 + fix/base-comun + CI en dev
- [ ] O5 PWA instalable con detección de conexión — offline backend en dev

## Trazabilidad Sprint 1 (entrega)

Resumen general del estado de los 4 equipos y la base común a fecha 2026-08-25, tras revertir #30 con #32.

| Equipo / Base | Módulo | Rama | PR a `dev` | Estado |
|---------------|--------|------|-----------|--------|
| Base común | Arranque backend + CORS + apiClient | `fix/base-comun` | **ABIERTO** | `dev` roto tras #30; parche de 4 archivos pendiente de merge |
| Grupo 1 | Mapa de necesidades | `dev` | #18, #22, #25 **MERGED** | En `dev`, datos reales |
| Grupo 2 | Alertas oficiales (GDACS) | `feature/alerts` | #56 **ABIERTO** | G2-only, filtro país ES→EN corregido, tests verdes |
| Grupo 3 | Voluntariado y donaciones | `dev` | #24, #27, #29 **MERGED** | En `dev`; falta UI donaciones |
| Grupo 4 | Personas / "estoy bien" + offline | `dev` | #20, #21 **MERGED** | En `dev`; falta UI offline |
| PM / Docs | Estado y gobernanza | `feature/docs` | **ABIERTO** | Crea tablero Kanban al mergear |

Nota: sin respuesta de la integradora y entrega mañana; si no hay merge de `fix/base-comun`, se mergea como parche de desbloqueo con esa justificación.

**Revisiones:** PR #56 (alertas, G2) abierto y pendiente de aprobaciones. `fix/base-comun` y `feature/docs` por abrir y revisar. **Grupo 4:** reparto de tareas aún pendiente (falta `docs/equipos/grupo4-tareas.md`).

## Pendientes de gobernanza (PM)
- [ ] Activar CI también en `dev` (hoy solo corre en `main`) — responsabilidad de Adriana.
- [ ] Votar la convención bilingüe (manifiesto la dejó "pendiente de votación").
- [ ] Mergear `feature/docs → dev` (crea el tablero Kanban y deja README bilingüe oficial).
- [ ] Cerrar la UI offline en el frontend (backend ya en `dev` vía #21).
- [ ] Limpiar `feature/alerts-vanessa` (rama duplicada de alertas).
- [ ] Preparar Demo Day (narrativa alerta→mapa→necesidad→recurso→resolución).
- [x] Decidir herramienta de backlog: Trello — decidido.
- [ ] Reparto de tareas del Grupo 4 pendiente (falta `docs/equipos/grupo4-tareas.md`).

## Abierto (por decidir)
- Zonas/celdas del mapa aún no definidas.
- Alcance exacto del modo offline (decisión abierta).
- Estrategia de despliegue (solo local hoy; CI sin despliegue).

## Riesgos
- **Alertas (G2, #56):** módulo núcleo fuera de `dev` en `feature/alerts` (G2-only tras revertir #30 con #32). Base común rota tras el revert: `dev` no arranca (falta `init_db`) ni conecta (CORS/`apiClient`) → parche en `fix/base-comun`. Conseguir aprobaciones (convenciones §6).
- **CI:** solo en `main`; `dev` sin protección de CI verde.
- **Rama duplicada:** `feature/alerts-vanessa` se solapa con `feature/alerts`.
