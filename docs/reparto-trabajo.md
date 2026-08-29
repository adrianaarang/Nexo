# Reparto de trabajo del equipo

Base común montada por Adriana (que debe ser revisada por un jefe de cada equipo) + 4 equipos.
Cada equipo tiene su propia pantalla y su propio backend, para que nadie se quede solo en
front o solo en backend y todos tengan algo que enseñar en la demo de forma independiente.

## Base común (ya montada)
- Punto de entrada de la app (`index.html`, menú, logo) y estilos generales (colores, tipografía, tarjetas, botones).
- Cliente que conecta frontend con backend (`apiClient.js`) — todos llaman a la API igual, sin `fetch()` propio.
- Arranque del servidor en Python (`main.py`, `config.py`) y conexión a BD con tablas ya creadas: `necesidades`, `voluntarios`, `donaciones`, `personas`.
- Datos de ejemplo (`seed.py`) para ver la app funcionando desde el día 1.

> Aún no hay PR de la base común; se pide que al menos una persona de cada equipo la revise.

## Equipo 1 — Necesidades
- Frontend: `frontend/pages/mapa.html` (formulario) y `frontend/js/core/mapa-necesidades/`.
- Backend: `backend/modules/necesidades/` (guardar, listar, estados, 8 categorías, intensidad).
- **Decidir:** categorías de necesidad; intensidad por conteo en el mapa.
- Nota: la visualización del mapa pasa al Equipo 4 (Mapa + Interfaz principal) en Sprint 2.

## Equipo 2 — Alertas + activación de crisis
- Frontend: `frontend/pages/alertas.html` y `frontend/js/core/alertas-oficiales/` (incluye `crisis.js`).
- Backend: `backend/modules/alertas/` e `backend/integrations/` (GDACS + Protección Civil).
- **Sprint 2:** activación de crisis (crear/activar/alto-riesgo/desactivar) y contrato mapa `{id, risk_level, status, zone}`.
- Ver detalle en `docs/equipos/grupo2-tareas.md`.

## Equipo 3 — Ayudas (unifica donación + voluntariado)
- Frontend: `frontend/pages/voluntariado.html`, `frontend/pages/donaciones.html` y `frontend/js/core/voluntariado-donaciones/`.
- Backend: `backend/modules/voluntariado/` y `backend/modules/donaciones/` (unificados en módulo Ayudas).
- **Decidir:** 3 tipos de ayuda (recursos, servicios, tiempo/voluntariado con nombre+DNI); marcar ayuda cubierta.
- Ver detalle en `docs/equipos/grupo3-tareas.md`.

## Equipo 4 — Mapa + Interfaz principal
Consume alertas y necesidades vía los contratos JSON y pinta la zona de alerta ALTO RIESGO.
- Frontend: `frontend/pages/mapa.html` + `frontend/js/core/mapa-necesidades/mapaNecesidades.js` (consumo de alertas y necesidades) e interfaz principal.
- Backend: comparte los contratos de `alertas` y `necesidades` (no implementa módulos propios salvo lo de mapa).
- **Decidir:** resaltado de zona ALTO RIESGO; intensidad por conteo (🟢🟠🔴).
- Ver detalle en `docs/equipos/grupo4-tareas.md`.
