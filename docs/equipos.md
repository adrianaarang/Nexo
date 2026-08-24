# Equipos de NEXO

Composición de los 4 equipos verticales + base común, según asignación del PM (Juan),
con los handles de GitHub confirmados en el registro del equipo (18/8/26).

Mapeo con los bloques del Kanban de GitHub (label `equipo-N` / `base-comun`).
Fuente de verdad: `docs/manifiesto.md` v1.0 (§7 y §8).

## Base común (Integradora)
- Dueña: **Adriana** (`adrianaarang`) — Integradora / repo owner.
- Revisada por al menos una persona de cada equipo antes del reparto (aún sin PR).

## Equipo 1 — Mapa de necesidades
- Bloque Kanban: `equipo-1` · Milestone: Sprint 1 (MVP)
- Scrum Master: **Josema** (`SiR0N`)
- Miembros:
  - Gema (`Gema-Villanueva`)
  - Helen (`HelenDiMo`) — *handle inferido del historial; no aparece en el registro, por confirmar*
  - Elena (`elenacarino-max`) — *en git también aparece `elenadiaz1`; posible cuenta alterna*
  - Adriana (`adrianaarang`)

## Equipo 2 — Alertas oficiales
- Bloque Kanban: `equipo-2` · Milestone: Sprint 1 (MVP) + Sprint 2
- Scrum Master: **Juan** (`juandelaf1`)
- Miembros:
  - Joel (`jowel2701`)
  - Luis (`luiselallali18-hub`)
  - Javi (`JCRbit`)
  - Vanessa (`garciaguadalupevanessa-bit`)

## Equipo 3 — Voluntariado y donaciones
- Bloque Kanban: `equipo-3` · Milestone: Sprint 1 (MVP)
- Scrum Master: **Laura** (`LauraSilRu`) — *pidió back-end y se unió a este equipo*
- Miembros:
  - Jose (`Gregdev08`)
  - Maria Isabel (`MariaIsaDurango`)
  - Maria Roldan (`Mary1922`)
  - Majo (`MajoRodri`)

## Equipo 4 — Personas y modo offline
- Bloque Kanban: `equipo-4` · Milestone: Sprint 1 (MVP) + Sprint 2
- Scrum Master: **Isabela** (`Isabela-Tellez`)
- Miembros:
  - Anas (`Anas28`)
  - Eli (`adryeli`)
  - Yohanna (`yohperez`)
  - David (`drojas-7u7`)

## Futuro — Resilience OS
- Bloque Kanban: `futuro` · Sin milestone (horizonte "A definir", manifiesto §7).
- Sin equipo asignado.

## Pendientes / a revisar (del registro)
- **Isabela**: tu asignación original y el manifiesto la ponen en **Grupo 4**, pero en el
  chat de Adriana aparece en **Grupo 2**. Mantengo Grupo 4 según tu asignación; confirmar.
- **MD Abdur (`5nhn007`)** aparece en el registro sin equipo asignado.
- **Helen**: handle no confirmado en el registro (se infirió `HelenDiMo`).
- **Elena**: doble rastro en git (`elenacarino-max` en registro, `elenadiaz1` en la rama
  `feature/form-cards-elenadiaz1`); aclarar cuál es el principal.

## Kanban en GitHub (resumen)
- Un issue "epic" por bloque, con checklist de tareas y decisiones abiertas.
- Labels: `base-comun`, `equipo-1`, `equipo-2`, `equipo-3`, `equipo-4`, `futuro`.
- Milestones: `Sprint 1 (MVP)`, `Sprint 2`.
- Tablero: columnas por **Status** (`To Do` / `In Progress` / `In Review` / `Done`),
  agrupado por **Label** (= bloque/equipo).

## Automatizacion (creacion al mergear)
Los issues se crean solos al mergear `feature/docs` -> `dev`, via
`.github/workflows/setup-kanban.yml` (usa `GITHUB_TOKEN`, sin permisos extra).
El script idempotente es `scripts/setup-kanban.sh`.
El tablero (Project V2) se crea manualmente en la cuenta del PM y se le anaden
las issues; la creacion del tablero no la hace el token de CI.

Al crearse, los issues de **Base común** y **Equipo 2 (alertas S1)** se cierran
automaticamente (trabajo ya completado). El resto se cierra solo al mergear sus
PR de integracion si estos incluyen `Closes #<num>`.
