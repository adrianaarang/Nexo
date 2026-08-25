# Grupo 1 (Mapa / Necesidades) — Distribución de tareas

Reparto del equipo 1 recibido de Josema (SM del grupo 1). Paralelo a `grupo2-tareas.md`.

## A. Reparto por persona
- [ ] **Elena — Base de datos y modelos** (`backend/modules/necesidades/models.py` + `schemas.py`): funciones de leer, crear y actualizar necesidades en la base de datos, y validación de campos. Es la pieza de la que dependen los endpoints.
- [ ] **Gema — Endpoints** (`backend/modules/necesidades/routes.py`): `GET` para listar, `POST` para crear y `PATCH` para cambiar el estado (abierta → en proceso → cubierta). Mientras Elena termina, puede empezar devolviendo datos inventados fijos y conectar los modelos reales después.
- [ ] **Adriana — Conexión front-back** (`frontend/js/core/mapa-necesidades/necesidadesApi.js`): funciones JS que llaman a la API. También le toca probar la integración completa cuando Elena y Gema terminen — es quien detecta si el contrato JSON no cuadra.
- [ ] **Josema — El mapa** (`mapa.html` + la parte de `mapaNecesidades.js` que pinta el mapa): Leaflet, marcadores con color según prioridad, popups, y el filtro por tipo si se decide hacerlo. Hasta que la API esté lista, puede trabajar con un array de necesidades inventadas en el propio archivo.
- [ ] **Helen — Formulario y tarjetas** (`necesidadCard.js` + la parte del formulario de `mapaNecesidades.js`): formulario de "reportar necesidad" con su validación, y cómo se ve cada necesidad en la lista lateral, incluyendo el botón de marcarla como cubierta.

## B. Coordinación y dependencias
- Los endpoints de Gema dependen de los modelos/schemas de Elena; Gema puede arrancar con mock fijo y enchufar lo real después.
- Josema y Helen pueden avanzar con datos inventados en el front hasta que Adriana termine `necesidadesApi.js` y la API real esté lista.
- Adriana es el punto de contrato JSON front-back: valida que el shape cuadre.

## C. Definition of Done (recordatorio)
Implementado · pytest/JS tests verdes · no rompe otros módulos · revisado en PR · demostrable en demo.
