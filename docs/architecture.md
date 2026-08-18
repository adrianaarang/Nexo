# Arquitectura de Nexo

## Visión general

```
frontend/ (HTML + CSS + JS, PWA)  <-- fetch/JSON -->  backend/ (Python, FastAPI)  <-- SQLite
                                                              |
                                                      integrations/
                                                       (GDACS, Protección Civil)
```

- El frontend es HTML/CSS/JS puro, sin build step ni framework: cada página
  (`frontend/pages/*.html`) carga su propio módulo JS.
- El backend expone una API REST bajo `/api/*`. Cada módulo (necesidades,
  alertas, voluntariado, donaciones, personas) es autocontenido: sus propias
  rutas, modelos y validaciones (`schemas.py`).
- La base de datos es SQLite (sin ORM) para mantener el proyecto simple en
  esta fase. `backend/db/migrations/001_init.sql` crea el esquema.

## Modo offline

1. El frontend intenta la petición normal (`apiClient.js`).
2. Si falla por falta de red, la acción se guarda en IndexedDB
   (`js/siguiente/modo-offline/localDb.js`) a través de `syncQueue.js`.
3. Cuando vuelve la conexión (evento `online` del navegador), `app.js` llama a
   `procesarColaPendiente()`, que envía todo lo pendiente a `POST /api/sync`.
4. El backend (`backend/sync/sync_controller.py`) aplica cada acción sobre el
   módulo correspondiente y registra un log en la tabla `sync_log`.

## Alertas

`backend/modules/alertas/services.py` combina dos fuentes: GDACS
(`integrations/gdacs_client.py`), que es la fuente principal y global, y
Protección Civil (`integrations/proteccion_civil_client.py`) como capa local
opcional. Si GDACS no responde (sin red, límite de peticiones), el módulo
devuelve una lista vacía en vez de romper el resto de la app.
