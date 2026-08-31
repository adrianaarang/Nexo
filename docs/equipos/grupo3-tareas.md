# Grupo 3 (Ayudas) — Distribución de tareas (Sprint 2)

Reparto del equipo 3 recibido de Laura (SM del grupo 3, `LauraSilRu`). En Sprint 2 **donación y
voluntariado se unifican en un módulo "Ayudas"** (3 tipos: recursos, servicios, tiempo/voluntariado).

## A. Reparto por persona
- [ ] **Laura S.R. — Backend Ayudas (voluntariado)** (`backend/modules/voluntariado/`): modelos, schemas, servicios y lógica de ayudas (recursos / servicios / tiempo).
- [ ] **María Isabel — Backend Ayudas (donaciones)** (`backend/modules/donaciones/`): persistencia de donaciones integrada como tipo de ayuda.
- [ ] **Majo — Frontend Donaciones/Ayudas** (`frontend/js/core/voluntariado-donaciones/`): página, formulario, listado, estados y estilos del lado de donaciones.
- [ ] **María — Frontend Voluntariado/Ayudas** (`frontend/js/core/voluntariado-donaciones/`): página, formulario de disponibilidad, listado, estados y estilos del lado de voluntariado.
- [ ] **José — Integración + QA**: integración de ramas, resolución de conflictos, coordinación técnica y tests del equipo.

## B. Coordinación y dependencias
- El backend unificado expone 3 tipos: `recursos`, `servicios`, `tiempo/voluntariado` (este último con `nombre` + `DNI`).
- Contrato hacia el mapa (G4): `{id, type, category, latitude, longitude, status}`.
- Se reusa la lógica de voluntariado/donaciones de Sprint 1.
- **Nota de estado (28/08):** los PRs #24, #27 y #29 (registro, config y disponibilidad de voluntariado) ya están en `dev`; falta unificar donaciones como tipo de ayuda y conectar `donaciones.js` al backend real.

## C. Definition of Done (recordatorio)
Implementado · pytest/JS tests verdes · no rompe otros módulos · revisado en PR · demostrable en demo.
