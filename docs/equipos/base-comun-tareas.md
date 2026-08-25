# Tareas de base común — pendientes

## Recuperar cambios de infraestructura en `dev`

- **Estado:** rama `fix/base-comun` → PR a `dev` (pendiente de merge por la integradora).
- **Responsable:** base común / integradora (Adriana).

### Cambios necesarios (4 archivos, solo infraestructura compartida)
1. `backend/db/database.py` — `init_db` idempotente (el backend no arranca sin esto).
2. `backend/config.py` — `CORS_ORIGINS` debe admitir también `http://127.0.0.1:5500`.
3. `frontend/js/shared/apiClient.js` — `API_BASE_URL` a `http://127.0.0.1:8000`.
4. `.gitignore` — tracking de `*.db` / `*.sqlite3`.

### Trazabilidad
- Rama: `fix/base-comun`
- PR: https://github.com/adrianaarang/Nexo/compare/dev...fix/base-comun
- Issue: crear en GitHub y asignar a base común (ver texto abajo).

### Issue sugerido (pegar en GitHub, asignar a base común)
**Título:** `fix(base-comun): init_db, CORS y apiClient para arrancar dev`

**Cuerpo:**
```
Se necesita un PR de base comun con estos 4 cambios para que dev funcione:
1. backend/db/database.py - init_db idempotente (el backend no arranca sin esto).
2. backend/config.py - CORS_ORIGINS debe admitir tambien http://127.0.0.1:5500.
3. frontend/js/shared/apiClient.js - API_BASE_URL apuntando a http://127.0.0.1:8000.
4. .gitignore - tracking de *.db / *.sqlite3.

Alcance: solo esos 4 archivos, sin tocar otros modulos.
Rama propuesta: fix/base-comun -> dev.
```
