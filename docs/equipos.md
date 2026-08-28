# Equipos de NEXO

Composición de los 4 equipos verticales + base común, según asignación del PM (Juan),
con los handles de GitHub confirmados en el registro del equipo (18/8/26).

Mapeo con los bloques del Kanban de GitHub (label `equipo-N` / `base-comun`).
Fuente de verdad: `docs/manifiesto.md` v1.0 (§7 y §8).

## Base común (Integradora)
- Dueña: **Adriana** (`adrianaarang`) — Integradora / repo owner.
- Revisada por al menos una persona de cada equipo antes del reparto (aún sin PR).

## Equipo 1 — Necesidades
- Bloque Kanban: `equipo-1` · Milestone: Sprint 2
- Scrum Master: **Josema** (`SiR0N`)
- Miembros:
  - Gema (`Gema-Villanueva`)
  - Helen (`HelenDiMo`) — *handle inferido del historial; no aparece en el registro, por confirmar*
  - Elena (`elenacarino-max`) — *en git también aparece `elenadiaz1`; posible cuenta alterna*
  - Adriana (`adrianaarang`)

## Equipo 2 — Alertas + activación de crisis
- Bloque Kanban: `equipo-2` · Milestone: Sprint 2
- Scrum Master: **Juan** (`juandelaf1`)
- Miembros:
  - Joel (`jowel2701`)
  - Luis (`luiselallali18-hub`)
  - Javi (`JCRbit`)
  - Vanessa (`garciaguadalupevanessa-bit`)

## Equipo 3 — Ayudas (unifica donación + voluntariado)
- Bloque Kanban: `equipo-3` · Milestone: Sprint 2
- Scrum Master: **Laura** (`LauraSilRu`) — *pidió back-end y se unió a este equipo*
- Miembros:
  - Jose (`Gregdev08`)
  - Maria Isabel (`MariaIsaDurango`)
  - Maria Roldan (`Mary1922`)
  - Majo (`MajoRodri`)

## Equipo 4 — Mapa + Interfaz principal
- Bloque Kanban: `equipo-4` · Milestone: Sprint 2
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
- **Isabela**: asignación confirmada en **Grupo 4** (Mapa + Interfaz principal) para Sprint 2, según el reparto final 27/08. Resuelto.
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

En Sprint 2 los issues se crean/actualizan con `scripts/setup-kanban.sh` (idempotente) al
mergear `feature/docs` -> `dev` (workflow `.github/workflows/setup-kanban.yml`). Los issues de
Sprint 1 obsoletos (#41, #43, #44) se cierran con trazabilidad hacia su equivalente de Sprint 2.
Cada issue de equipo se cierra solo al mergear el PR de integracion del grupo si incluye `Closes #<num>`.
