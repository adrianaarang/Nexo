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

## Equipo 1 — Mapa de necesidades
Módulo con más votos en la encuesta (50%); pantalla principal.
- Frontend: `frontend/pages/mapa.html` y `frontend/js/core/mapa-necesidades/`.
- Backend: `backend/modules/necesidades/` (guardar, listar, cambiar estado abierta→cubierta).
- **Decidir:** cómo se define la prioridad de una necesidad; si el mapa filtra por tipo.

## Equipo 2 — Alertas oficiales
- Frontend: `frontend/pages/alertas.html` y `frontend/js/core/alertas-oficiales/`.
- Backend: `backend/modules/alertas/` e `backend/integrations/` (GDACS mundial + hueco para Protección Civil local).
- **Decidir:** qué mostrar sin alertas activas; si conviene cachear respuesta de GDACS.
- Ver detalle en `docs/equipos/grupo2-alertas.md`.

## Equipo 3 — Voluntariado y donaciones
- Frontend: `frontend/pages/voluntariado.html`, `frontend/pages/donaciones.html` y `frontend/js/core/voluntariado-donaciones/`.
- Backend: `backend/modules/voluntariado/` y `backend/modules/donaciones/`.
- **Decidir:** cómo marcar una donación ya cubierta; si un voluntario puede marcarse como asignado.

## Equipo 4 — Personas y modo sin conexión
Van juntas porque el registro de personas es el caso que más necesita funcionar sin internet.
- Frontend: `frontend/pages/personas.html`, `frontend/pages/estoy-bien.html` y `frontend/js/siguiente/` (registro de personas + modo offline).
- Backend: `backend/modules/personas/` y `backend/sync/`.
- **Decidir:** qué pasa si dos personas reportan a la misma desaparecida por separado; cómo probar el modo sin conexión (modo avión del móvil).
