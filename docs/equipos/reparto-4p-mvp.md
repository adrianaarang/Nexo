# Reparto 4 personas — MVP Jueves (versión particular)

> Tras la partición del proyecto en 4 versiones particulares, este equipo de 4 mantiene el mismo proyecto NEXO pero con 1 persona por módulo vertical. Cada persona es dueña E2E de su módulo (frontend + backend + tests) para demo. Reemplaza al reparto 5×4 anterior (ver `grupo1-4-tareas.md` S1). Sprint 2 final 27/08: G1=Necesidades, G2=Alertas, G3=Ayudas, G4=Mapa — se mantiene.

## Principio
- **Vertical por módulo**, no por capa. Nadie toca archivos ajenos sin avisar (ver `docs/convenciones.md` § propiedad).
- **MVP primero**: mapa + alerta + zona ALTO RIESGO + necesidad + 1 ayuda en BD. Capas, intensidad, GDACS y PWA son Siguiente.
- **Integración diaria 15:00** en `dev`. Orden de merge para evitar conflictos: P1 (Alertas) → P2 (Necesidades) → P3 (Ayudas) → P4 (Mapa consume).

## Asignación (4p) — Equipo: Javi, Juan, Luis, Vanessa

### P1 — Javi (G2 Alertas — Backend + Filtros)
**Dueño de:** `backend/modules/alertas/services.py`, `routes.py`, `backend/config.py` (CORS), `backend/integrations/gdacs*`
**Rol previo G2:** filtros tipo/severidad/país + orden por fecha. Mantiene backend.
**MVP:**
- [ ] Mergear rama `alerts` (da97f22) a `dev` — RiskLevelEnum + zona GeoJSON
- [ ] Endpoints: `GET /api/alerts` con filtros + `POST /api/alertas/{id}/alto-riesgo` + contrato `{id, risk_level, status, zone}` + fallback GDACS `[]`
- [ ] Tests `tests/backend/test_alertas.py` verdes

### P2 — Juan (G4 Mapa + Interfaz + GeoRisk — tu especialidad)
**Dueño de:** `frontend/pages/mapa.html`, `frontend/js/core/mapa-necesidades/mapaNecesidades.js`, `frontend/js/shared/apiClient.js`, `frontend/css/*`, `frontend/mocks/*.json`, `georisk_globe/` (referencia), `src/h3_aggregator.py` (referencia)
**Rol previo:** GeoRisk globo/mapa. Maximiza tu expertise.
**MVP:**
- [ ] Leaflet/MapLibre base + capas: Alertas / Zonas / Necesidades / Ayudas (toggle)
- [ ] Consumir contratos G1 `{id, type, lat, lon, status, direccion}` y G2 `{id, risk_level, status, zone}` vía `apiClient.js`
- [ ] Resaltar `zone` cuando `risk_level=high` (ALTO RIESGO) + intensidad 🟢🟠🔴 por conteo (usa `frontend/mocks/` si API no lista)
- [ ] Interfaz principal `Mapa | Alertas | Ayudas` + popups. Post-MVP: H3 res 6 y globo con `h3_aggregator.py`

### P3 — Luis (G1 Necesidades + G2 GDACS/Cache)
**Dueño de:** `backend/modules/necesidades/*`, `frontend/js/core/mapa-necesidades/formularioNecesidad.js`, `necesidadCard.js`, `necesidadesApi.js`, `geocodificacion.js`, `backend/integrations/gdacs_client.py` (cache)
**Rol previo G2:** `gdacs_client.py` + cache TTL 15 min. Traslada lógica a Necesidades.
**Estado:** backend rediseño 8 cats/2 estados + `direccion` ya en `dev` (91a7647). **Solo pulir frontend.**
**MVP:**
- [ ] Validar `POST /api/necesidades` con `direccion` + estados `abierta→cubierta`
- [ ] Formulario 8 categorías + tarjeta lateral "cubierta" + `geocodificacion.js`
- [ ] Conectar `necesidadesApi.js` al backend real y asegurar `GET` lista

### P4 — Vanessa (G3 Ayudas + GDACS/PC + Estilos)
**Dueño de:** `backend/modules/voluntariado/*`, `backend/modules/donaciones/*`, `frontend/pages/donaciones.html`/`voluntariado.html`, `frontend/js/core/voluntariado-donaciones/**`, `frontend/css/alertas.css`, `backend/integrations/proteccion_civil*`
**Rol previo G2:** estilos `alertas.css` + tests + PC. Mantiene UI.
**Estado:** backend #24, #27, #29 en `dev`, falta unificación.
**MVP (reduce a 1 tipo):**
- [ ] Crear wrapper `POST /api/ayudas` + `GET /api/ayudas` (3 tipos: recursos/servicios/tiempo con DNI) — reutiliza modelos
- [ ] UI `ayudas.html` con selector + formulario mínimo
- [ ] Contrato hacia mapa G4: `{id, type, category, latitude, longitude, status}`

## Orden de integración (evita pisarse) — con nombres
1. **Javi (G2)** mergea Alertas a `dev` primero (toca `main.py`, `config.py` si hace falta — avisar)
2. **Luis (G1) y Vanessa (G3)** en paralelo sobre `dev` actualizado (no tocan `alertas/` ni `mapa.html`)
3. **Juan (G4)** último: consume APIs de todos, solo toca `mapa.html`/`mapaNecesidades.js`/`mocks` + `apiClient.js`
4. Daily 15:00: `git pull --rebase origin dev` antes de push; PRs con `Closes #<num>` para Kanban. **Juan coordina daily y PR final** (capitán G2 previo).

## Qué dejar fuera hasta después de jueves
H3 hexagonal fino (res 7+), globo 3D (`georisk_globe/`), clustering/ML, PWA offline UI completa, red mesh/satélite. GeoRisk como fuente única y Vercel se evalúan post-MVP.

## Demo guion (5 min)
Georisk/Alertas: Gestor crea alerta → delimita zona → ALTO RIESGO → Mapa resalta zona → Necesidades aparecen (intensidad) → Ayuda disponible dentro de zona → Marcar necesidad cubierta.

## Ramas sugeridas (4p)
- `feat/alertas-g2` (P1, desde `alerts`)
- `feat/necesidades-g1-polish` (P2)
- `feat/ayudas-g3-unifica` (P3)
- `feat/mapa-g4-capas` (P4)
Todas → `dev` con PR y 1 review de otro miembro del equipo de 4.
