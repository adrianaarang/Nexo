# Grupo 1 (Necesidades) — Distribución de tareas (Sprint 2)

Reparto del equipo 1 recibido de Josema (SM del grupo 1). En Sprint 2 el **mapa** pasa al
Equipo 4; el Grupo 1 se queda con el módulo de **Necesidades** (datos, backend y formulario).

## A. Reparto por persona
- [ ] **Elena — Modelos y schemas** (`backend/modules/necesidades/models.py` + `schemas.py`): estados (`abierta` → `en_proceso` → `cubierta`), 8 categorías y validación de campos.
- [ ] **Gema — Endpoints** (`backend/modules/necesidades/routes.py`): `GET` listar, `POST` crear y `PATCH` cambiar estado; filtros y paginación.
- [ ] **Adriana — Conexión front-back** (`frontend/js/core/mapa-necesidades/necesidadesApi.js`): funciones JS que llaman a la API; valida el contrato JSON con el mapa.
- [ ] **Helen — Formulario y tarjetas** (`necesidadCard.js` + formulario de `mapaNecesidades.js`): reportar necesidad, validación, y vista en la lista lateral con botón "cubierta".
- [ ] **Josema — Intensidad y UI de necesidades en el mapa**: color/intensidad por conteo, popups; coordina con G4 el resaltado en el mapa.

## B. Coordinación y dependencias
- Los endpoints de Gema dependen de los modelos/schemas de Elena; Gema puede arrancar con mock fijo.
- Helen y Josema pueden avanzar con datos inventados hasta que la API real esté lista.
- Adriana es el punto de contrato JSON front-back.
- Contrato hacia el mapa (G4): `{id, type, latitude, longitude, status}`.

## C. Definition of Done (recordatorio)
Implementado · pytest/JS tests verdes · no rompe otros módulos · revisado en PR · demostrable en demo.
