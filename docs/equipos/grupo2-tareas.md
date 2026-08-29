# Grupo 2 (Alertas + activación de crisis) — Distribución de tareas (Sprint 2)

Documento de trabajo del capitán (Juan) para revisar y cerrar el módulo de alertas con el equipo.
No modifica el repo remoto: es guion + checklist para usar en la reunión.

> **Sprint 2 — Activación de crisis:** el backend gestor (crear / activar / alto-riesgo / desactivar)
> ya está implementado y subido en la rama `alertas` (Juan). Contrato hacia el mapa:
> `{id, risk_level, status, zone}`. ALTO RIESGO desbloquea necesidades/ayudas en la zona.

## A. Guion para la reunión de equipo (10–15 min)
1. **Estado rápido:** backend de alertas completo en `feature/alerts` (endpoint, filtros, caché,
   tests). Frontend en `juan/alerts-frontend` (cliente API, estados, pantalla). Contrato
   `/api/alertas?tipo=&severidad=&pais=` ya alineado entre front y back.
2. **Decisions cerradas (D1–D4):** repasarlas y confirmar que el código las respeta
   (caché 15 min, estado vacío, filtros, Protección Civil en TODO).
3. **Repaso de reparto:** cada persona confirma su slice (Luís/Javi backend, Juan
   frontend+estados+revisión, Joel pantalla+render, Vanessa estilos+test).
4. **Integración:** plan de unir backend+frontend y probar E2E en local (caso C3 del plan).
5. **Cierre:** definición de Done, quién abre el PR, y que **Juan (capitán) revisa y mergea**
   el PR del equipo (convenciones §6). Avisar a Adriana para el merge `feature/*` → `dev`
   (integradora/rotativo, §21).

## B. Checklist de tareas (revisar / hacer)
**Backend**
- [ ] `gdacs_client.py` implementado (Luís): GET RSS, mapeo a modelo Nexo, fallback `[]` si falla
- [ ] Caché TTL 15 min en memoria (Luís) — configurable en `config.py`
- [ ] `services.py` con filtros tipo/severidad/pais y orden por fecha (Javi)
- [ ] `routes.py` `GET /api/alertas` con query params (Javi)
- [ ] `tests/backend/test_alertas.py` en verde (Javi)

**Frontend**
- [ ] `alertasApi.js` usa `apiGet` con contrato (Juan)
- [ ] `estadosAlertas.js`: carga / vacío (D2) / error (Juan)
- [ ] `alertas.html` + `alertas.js`: pantalla, filtros y render con `crearTarjeta`+badge (Joel)
- [ ] `css/alertas.css` con variables `nexo-`, sin colores nuevos (Vanessa)
- [ ] `tests/frontend/alertas.test.js` (Vanessa)

**Cierre del equipo**
- [ ] Integrar E2E y demo local (Joel + Juan)
- [ ] Abrir PR desde la rama del equipo
- [ ] Juan (capitán) revisa y mergea el PR del equipo
- [ ] Verificar **CI verde** en el PR (obligatorio, conv §6)
- [ ] Avisar a Adriana para mergear `feature/*` → `dev`

## C. Definition of Done (recordatorio)
Implementado · pytest verde · no rompe otros módulos · revisado en PR · demostrable en demo.

## D. Trazabilidad actual (entrega Sprint 1)

**Módulo alertas (G2) — `feature/alerts` → `dev`**
- PR solo con alcance G2: `backend/modules/alertas`, integraciones GDACS/Protección Civil, frontend `alertas-oficiales`, `alertas.html`, tests (`test_alertas.py` JCRbit, `alerts.test.js` Vanessa).
- Fix de filtrado: `readFilters()` alinea claves con `getAlerts()` y se normaliza país ES→EN (GDACS).
- Router ya cableado en `main.py`. Excluye `database.py` / `config.py` / `apiClient.js` / `.gitignore` (base común).
- Estado: pendiente de merge por integradora.

**Base común (stopgap G2, dev roto) — `fix/base-comun` → `dev`**
- Motivo: tras revertir #30, `dev` no arranca (`init_db`) y el front no conecta (CORS / `apiClient`).
- 4 archivos: `backend/db/database.py` (init_db idempotente), `backend/config.py` (CORS `127.0.0.1:5500`), `frontend/js/shared/apiClient.js` (API `127.0.0.1:8000`), `.gitignore` (tracking `*.db`).
- Estado: pendiente de merge. Issue sugerido para base común:
  - **Título:** `fix(base-comun): init_db, CORS y apiClient para arrancar dev`
  - **Cuerpo:** PR de base comun con 4 cambios (database.py init_db idempotente; config.py CORS 127.0.0.1:5500; apiClient.js API 127.0.0.1:8000; .gitignore tracking *.db). Alcance: solo esos 4 archivos. Rama: `fix/base-comun` → `dev`.
  - Nota: sin comunicación con la integradora y entrega mañana; si no hay merge, el PR se mergea como parche de desbloqueo con esa justificación.

## E. Sprint 2 — Estado de activación de crisis (actualizado 28/08)
- Backend gestor implementado en `backend/modules/alertas/` (`models.py`, `schemas.py`, `routes.py`, `services.py`) y migración `004_alertas_gestor.sql`; rama `alertas` (Juan).
- Endpoints: `POST /api/alertas`, `GET`, `GET/{id}`, `PATCH/{id}`, `POST/{id}/activar`, `POST/{id}/alto-riesgo`, `POST/{id}/desactivar`.
- Tests de backend: `tests/backend/test_alertas_routes.py` (13 en verde).
- Pendiente front (Javi): `alertas.html` + `crisis.js` (activación); pendiente integración GDACS/PC (Vanessa).
- Cerrar este issue de equipo con `Closes #<num>` al mergear el PR de integración de G2.
