# Grupo 1 (Necesidades) — Distribución de tareas (Sprint 2)

Reparto del equipo 1 recibido de Josema (SM del grupo 1). En Sprint 2 el **mapa** pasa al
Equipo 4; el Grupo 1 se queda con el módulo de **Necesidades** (datos, backend y formulario).

## A. Reparto por persona
- [x] **Elena — Modelos y schemas** (`backend/modules/necesidades/models.py` + `schemas.py`): 8 categorías (agua/alimentos/parafarmacia/ropa/higiene/refugio/transporte/otros) + estados `abierta`→`cubierta` + campo `direccion` + validación — **mergeado en `dev` (PR #56, 4c3d244)**.
- [x] **Gema — Endpoints + services** (`backend/modules/necesidades/routes.py` + `services.py`): `GET` listar, `POST` crear y `PATCH` estado + `services.py` (lógica) — **mergeado en `dev` (PR #61, 91a7647)**.
- [ ] **Adriana — Conexión front-back** (`frontend/js/core/mapa-necesidades/necesidadesApi.js` + `geocodificacion.js`): funciones JS que llaman a la API + geocodificación — verificado en integración (pendiente marcar done tras tests).
- [ ] **Helen — Formulario y tarjetas** (`necesidadCard.js` + `formularioNecesidad.js`): formulario simplificado (categoría + ubicación + `direccion` legible), validación y vista en lista con botón "cubierta" — rediseño 8 cats, mergeado en `dev`.
- [ ] **Josema — Intensidad y UI de necesidades en el mapa**: color/intensidad por conteo, popups; coordina con G4 el resaltado en el mapa.

## B. Coordinación y dependencias
- Los endpoints de Gema dependen de los modelos/schemas de Elena; Gema puede arrancar con mock fijo.
- Helen y Josema pueden avanzar con datos inventados hasta que la API real esté lista.
- Adriana es el punto de contrato JSON front-back.
- Contrato hacia el mapa (G4): `{id, type, latitude, longitude, status, direccion}` (con `direccion` legible desde rediseño).

## C. Definition of Done (recordatorio)
Implementado · pytest/JS tests verdes · no rompe otros módulos · revisado en PR · demostrable en demo.
