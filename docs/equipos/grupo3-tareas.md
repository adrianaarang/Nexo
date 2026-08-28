# Grupo 3 (Voluntariado y Donaciones) - Distribución de tareas

Reparto del equipo 3 recibido de Laura (SM del grupo 3, `LauraSilRu`). Paralelo a `grupo1-tareas.md` y `grupo2-tareas.md`.

## A. Reparto por persona
- [ ] **Laura S.R. — Backend Voluntariado** (`backend/modules/voluntariado/`): API, modelos, schemas, servicios, validaciones, configuración y lógica del módulo de voluntariado.
- [ ] **María — Frontend Voluntariado** (`frontend/js/core/voluntariado-donaciones/`): página, formulario, disponibilidad, listado, estados, integración con API y estilos del lado de voluntariado.
- [ ] **Majo — Frontend Donaciones** (`frontend/js/core/voluntariado-donaciones/`): página, formulario, listado, lógica, API client y estilos del módulo de donaciones.
- [ ] **María Isabel — Backend Donaciones** (`backend/modules/donaciones/`): API, modelos, lógica y persistencia del módulo de donaciones.
- [ ] **José — Integración + QA**: integración de ramas, resolución de conflictos, coordinación técnica y tests del equipo.

## B. Coordinación y dependencias
- El backend de voluntariado (Laura) y el de donaciones (María Isabel) son los contratos de los que dependen los fronts correspondientes.
- María (front voluntariado) y Majo (front donaciones) pueden avanzar con mocks hasta que los backends expongan los endpoints reales; luego enchufan el API client.
- José centraliza la integración de ramas y los tests E2E/QA antes del PR del equipo.
- **Nota de estado (26/08):** los PRs #24, #27 y #29 (registro, config y disponibilidad de voluntariado) ya están mergeados en `dev`; falta conectar `donaciones.js` al backend real de donaciones (María Isabel + Majo).

## C. Definition of Done (recordatorio)
Implementado · pytest/JS tests verdes · no rompe otros módulos · revisado en PR · demostrable en demo.
