# Backlog de NEXO

> Mantenido por el Product Manager (Juan). Última actualización: 2026-08-31 (merge PR #53, #56 y #61 — `dev` en 91a7647; rediseño Necesidades 8 cats/2 estados en `dev`).
> Referencia de prioridades: `docs/manifiesto.md` y `docs/roadmap.md`.

## Estado por módulo

| Módulo | Prioridad | Rama(s) | PR | Dueño | Estado |
|--------|-----------|---------|----|-------|--------|
| Alertas oficiales | Núcleo (MVP) | `feature/alerts`, `fix/base-comun` | #56 **ABIERTO** (feature/alerts→dev, G2-only) · `fix/base-comun`→dev **ABIERTO** | Grupo 2 (Juan, capitán) | Backend + pantalla + tests en verde (feature/alerts, G2-only tras revertir #30 con #32). Base común separada en `fix/base-comun` (dev no arranca tras revertir #30). |
| Mapa de necesidades / Necesidades | Núcleo (MVP) | `dev` | #18, #22, #25, #61, #56 **MERGED** | Grupo 1 (Josema + Gema/Helen/Elena/Adriana) | En `dev`: rediseño 8 categorías/2 estados + `direccion` + geocodificación + `services.py`. PRs #61 y #56 mergeados 91a7647. |
| Voluntariado y donaciones | Núcleo (MVP) | `dev` | #24, #27, #29 **MERGED** | Grupo 3 | En `dev`: registro + disponibilidad + config/soporte. Falta conectar `donaciones.js` al backend real. |
| Registro de personas / "estoy bien" | Siguiente | `dev` | #20 **MERGED** | Transversal (S1: Grupo 4) | En `dev`: backend "estoy bien" (45 tests). **Sprint 1**. |
| Modo offline (PWA) | Siguiente | `dev` | #21 **MERGED** (backend) | Transversal (S1: Grupo 4) | Backend de sincronización en `dev`; falta UI offline en frontend. |
| Documentación y gobernanza | Transversal | `dev` | #53 **MERGED** (91a7647) | PM (Juan) | README bilingüe, `equipos.md`, `equipos/grupo*-tareas.md`, ER + Kanban — mergeado vía #53. |

> **Mapeo de grupos actualizado en Sprint 2 (reunión 27/08):** G1=Necesidades, G2=Alertas, G3=Ayudas, G4=Mapa + Interfaz principal. En Sprint 1 eran G1=Mapa de necesidades, G2=Alertas, G3=Voluntariado/Donaciones, G4=Personas/Offline. La sección "Trazabilidad Sprint 1" más abajo mantiene el detalle anterior para trazabilidad.

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
| #53 | docs(sprint2): align team/module mapping and regenerate Kanban (Sprint 2) | **MERGED** a `dev` (91a7647) — cierra #41/#43/#44 con trazabilidad |
| #55 | feature/forms-needs-elenadiaz1 | **MERGED** a `dev` (88019a1) |
| #56 | feat(necesidades): nueva_version/elena — 8 cats + direccion | **MERGED** a `dev` (4c3d244) |
| #61 | feat(necesidades): gema — rediseño 2 estados + services | **MERGED** a `dev` (91a7647) |
| `fix/base-comun`→dev | fix(base-comun): init_db, CORS and apiClient to boot dev | **MERGED** (vía #53 / ya en dev) |

## Tablero / Kanban (Sprint 2)

En Sprint 2 el Kanban se regenera con `scripts/setup-kanban.sh` (idempotente) al mergear
`feature/docs → dev` (workflow `.github/workflows/setup-kanban.yml`, usa `GITHUB_TOKEN`). Crea
los epics por equipo (Necesidades, Alertas+activación, Ayudas, Mapa+Interfaz) y **cierra con
trazabilidad** los issues de Sprint 1 obsoletos (#41, #43, #44) hacia su equivalente de Sprint 2.
Cada epic se cierra al mergear el PR de integración del grupo si incluye `Closes #<num>`. El
tablero visual es un Project V2 personal del PM (agrupado por Label = equipo, columnas por Status).
Composición de equipos en `docs/equipos.md`.

Mapeo Sprint 2 (reparto final 27/08):

| Equipo | Módulo | Rama sugerida | Estado |
|--------|--------|---------------|--------|
| Equipo 1 | Necesidades | `feature/necesidades/*` | Por hacer |
| Equipo 2 | Alertas + activación de crisis | `alerts` (backend hecho) | Backend en `alerts`; falta front (Javi) + GDACS/PC (Vanessa) |
| Equipo 3 | Ayudas (donación + voluntariado) | `feature/ayudas/*` | Por hacer |
| Equipo 4 | Mapa + Interfaz principal | `feature/mapa/*` | Por hacer |

> Los issues de Sprint 1 (#41 Equipo 1, #43 Equipo 3, #44 Equipo 4) se cierran al crear los de
> Sprint 2, con un comentario de trazabilidad hacia el nuevo issue.

### Sprint 1 (histórico) — issues originales del Kanban

> Snapshot 2026-08-25. El script de Sprint 2 cierra estos issues con trazabilidad:
> #41 → Equipo 1 - Necesidades, #43 → Equipo 3 - Ayudas, #44 → Equipo 4 - Mapa + Interfaz.

| # | Título (Sprint 1) | Label | Estado a 2026-08-25 |
|---|-------------------|-------|---------------------|
| #40 | Base comun - revision previa al reparto | base-comun, kanban | **CERRADO** |
| #41 | Equipo 1 - Mapa de necesidades | equipo-1, kanban | Abierto |
| #42 | Equipo 2 - Alertas oficiales | equipo-2, kanban | **CERRADO** |
| #43 | Equipo 3 - Voluntariado y donaciones | equipo-3, kanban | Abierto |
| #44 | Equipo 4 - Personas y modo offline | equipo-4, kanban | Abierto |
| #45 | Futuro - Resilience OS | futuro, kanban | Abierto |

## Objetivos MVP (de `docs/manifiesto.md`)
- [ ] O1 Alertas GDACS con filtros y estados (núcleo del Grupo 2) — feature/alerts (G2) listo, falta PR #56 a dev; base común en fix/base-comun
- [ ] O2 Mapa de necesidades end-to-end — en dev
- [ ] O3 Voluntariado/donaciones end-to-end — backend en dev; falta UI donaciones
- [ ] O4 E2E completo (frontend→API→BD) con CI verde — depende de #56 + fix/base-comun + CI en dev
- [ ] O5 PWA instalable con detección de conexión — offline backend en dev

## Trazabilidad Sprint 1 (entrega) — snapshot 2026-08-25

Resumen general del estado de los 4 equipos y la base común a fecha 2026-08-25, tras revertir #30 con #32. Se mantiene por trazabilidad; el estado actual está en "Estado por módulo" arriba.

| Equipo / Base | Módulo | Rama | PR a `dev` | Estado a 2026-08-25 |
|---------------|--------|------|-----------|---------------------|
| Base común | Arranque backend + CORS + apiClient | `fix/base-comun` | **ABIERTO** | `dev` roto tras #30; parche de 4 archivos pendiente de merge |
| Grupo 1 | Mapa de necesidades | `dev` | #18, #22, #25 **MERGED** | En `dev`, datos reales |
| Grupo 2 | Alertas oficiales (GDACS) | `feature/alerts` | #56 **ABIERTO** | G2-only, filtro país ES→EN corregido, tests verdes |
| Grupo 3 | Voluntariado y donaciones | `dev` | #24, #27, #29 **MERGED** | En `dev`; falta UI donaciones |
| Grupo 4 | Personas / "estoy bien" + offline | `dev` | #20, #21 **MERGED** | En `dev`; falta UI offline |
| PM / Docs | Estado y gobernanza | `feature/docs` | **ABIERTO** | Crea tablero Kanban al mergear |

> Nota histórica: sin respuesta de la integradora y entrega al día siguiente; `fix/base-comun` se mergeó después como parte de #53.

## Trazabilidad Sprint 2 (actual — `dev` en 91a7647)

| Equipo / Base | Módulo | Rama | PR a `dev` | Estado actual |
|---------------|--------|------|-----------|---------------|
| Base común | Arranque backend + CORS + apiClient | `dev` | #53 **MERGED** | En `dev`; `dev` arranca (init_db idempotente + CORS + apiClient) |
| Grupo 1 | Necesidades (8 cats, 2 estados) | `dev` | #61, #56 **MERGED** | En `dev`: rediseño 8 cats + `direccion` + `services.py` + geocodificación + 2 estados — merge 91a7647 |
| Grupo 2 | Alertas oficiales (GDACS) | `feature/alerts` | #56 (S1) — pendiente | Aún fuera de `dev` (G2-only tras revertir #30); PR #56 pendiente de integrar |
| Grupo 3 | Ayudas (voluntariado/donaciones) | `dev` | #24, #27, #29 **MERGED** | En `dev`; falta UI donaciones |
| Grupo 4 | Mapa + Interfaz principal | `dev` | #53 **MERGED** (docs) | En `dev`: `grupo4-tareas.md` creado; mapa consume contratos alertas/necesidades |
| PM / Docs | Estado y gobernanza | `dev` | #53 **MERGED** | ER + Kanban + docs S2 en `dev` |

## Pendientes de gobernanza (PM)
- [ ] Integrar `feature/alerts` (G2) a `dev` (PR #56 pendiente) — alertas aún fuera de `dev` tras revertir #30.
- [ ] Cerrar la UI offline en el frontend (backend ya en `dev` vía #21).
- [ ] Limpiar ramas duplicadas `feature/alerts-vanessa` / `fix/base-comun` (ya sin upstream, solo locales).
- [ ] Preparar Demo Day (narrativa alerta→mapa→necesidad→recurso→resolución).
- [x] Activar CI también en `dev` — hecho (workflow en `dev`, pendiente verificar checks).
- [x] Mergear `feature/docs → dev` — mergeado #53 en 91a7647 (crea tablero Kanban y deja README bilingüe oficial).
- [x] Decidir herramienta de backlog: Trello — decidido.
- [x] Reparto de tareas del Grupo 4 — creado `docs/equipos/grupo4-tareas.md` en Sprint 2.
- [x] Votar la convención bilingüe (README bilingüe oficial en `dev`).

## Abierto (por decidir)
- Zonas/celdas del mapa aún no definidas.
- Alcance exacto del modo offline (decisión abierta).
- Estrategia de despliegue (solo local hoy; CI sin despliegue).

## Riesgos
- **Alertas (G2, #56):** módulo aún fuera de `dev` (G2-only tras revertir #30). `fix/base-comun` ya mergeado vía #53, pero `feature/alerts` sigue pendiente de integrar a `dev`.
- **CI:** activado en `dev` (#53), pero `dev` sigue sin protección de branch con checks requeridos.
- **Rama duplicada:** `feature/alerts-vanessa` / `fix/base-comun` ya sin upstream; limpiar locales.
