# Reparto 4 personas — MVP Jueves (versión particular)

> Tras la partición del proyecto en 4 versiones particulares, este equipo de 4 mantiene el mismo proyecto NEXO pero con 1 persona por módulo vertical. Cada persona es dueña E2E de su módulo (frontend + backend + tests) para demo. Reemplaza al reparto 5×4 anterior (ver `grupo1-4-tareas.md` S1). Sprint 2 final 27/08: G1=Necesidades, G2=Alertas, G3=Ayudas, G4=Mapa — se mantiene.

## Principio
- **Vertical por módulo**, no por capa. Nadie toca archivos ajenos sin avisar (ver `docs/convenciones.md` § propiedad).
- **MVP primero**: mapa + alerta + zona ALTO RIESGO + necesidad + 1 ayuda en BD. Capas, intensidad, GDACS y PWA son Siguiente.
- **Integración diaria 15:00** en `dev`. Orden de merge para evitar conflictos: P1 (Alertas) → P2 (Necesidades) → P3 (Ayudas) → P4 (Mapa consume).

## Asignación (4p)

### P1 — Juan (G2 Alertas + Coordinación + Base común)
**Dueño de:** `backend/modules/alertas/*`, `backend/integrations/gdacs*`, `frontend/pages/alertas.html`, `frontend/js/core/alertas-oficiales/**`, `api/index.py` (Vercel), `tests/backend/test_alertas*`
**MVP:**
- [ ] Mergear rama `alerts` (da97f22) a `dev` — ya con RiskLevelEnum y zona GeoJSON
- [ ] Adaptar a esquema unificado GeoRisk (si se decide Vercel): `external_id`, `source`, `severity`, `risk_level`, `zone`, `is_active`, fallback `[]` GDACS
- [ ] Endpoints: `GET /api/alerts`, `POST /api/alertas`, `POST /api/alertas/{id}/activar|alto-riesgo|desactivar` + contrato `{id, risk_level, status, zone}`
- [ ] Tests 13 verdes + activar `crisis.js` (Javi) y GDACS/PC (Vanessa) si da tiempo — mínimo manual
- [ ] Coordinar daily, resolver conflictos, PR final y seed demo

### P2 — Necesidades (G1)
**Dueño de:** `backend/modules/necesidades/*`, `frontend/js/core/mapa-necesidades/formularioNecesidad.js`, `necesidadCard.js`, `necesidadesApi.js`, `geocodificacion.js`, `tests/backend/test_necesidades*`, `tests/frontend/mapa-necesidades.test.js`
**Estado:** backend rediseño 8 cats/2 estados + `direccion` ya en `dev` (91a7647). **Solo pulir frontend.**
**MVP:**
- [ ] Validar `POST /api/necesidades` con `direccion` legible (geocodificación) + estados `abierta→cubierta`
- [ ] Formulario simplificado 8 categorías funciona + tarjeta lateral con botón "cubierta"
- [ ] Conectar `necesidadesApi.js` al backend real (quitar mocks) y asegurar `GET` lista
- [ ] Tests verdes (ya hay `probar_integracion_necesidades.mjs`)

### P3 — Ayudas (G3) — Unifica donación + voluntariado
**Dueño de:** `backend/modules/voluntariado/*`, `backend/modules/donaciones/*`, `frontend/pages/donaciones.html`, `frontend/pages/voluntariado.html`, `frontend/js/core/voluntariado-donaciones/**`
**Estado:** backend #24, #27, #29 en `dev`, falta unificación y UI conectada.
**MVP (reduce alcance a 1 tipo para demo):**
- [ ] Crear wrapper `POST /api/ayudas` + `GET /api/ayudas` (3 tipos: recursos/servicios/tiempo con nombre+DNI) — reutiliza modelos existentes
- [ ] UI `ayudas.html` con selector tipo + formulario mínimo (para tiempo: nombre+DNI)
- [ ] Contrato hacia mapa G4: `{id, type, category, latitude, longitude, status}` y persistencia
- [ ] Si falta tiempo: hardcodear 1 ayuda `recurso: alimentos` en `seed.py` y mostrarla en mapa

### P4 — Mapa + Interfaz principal (G4)
**Dueño de:** `frontend/pages/mapa.html`, `frontend/js/core/mapa-necesidades/mapaNecesidades.js`, `frontend/css/*`, `frontend/mocks/*.json`
**Estado:** mapa base existe pero sin capas dinámicas.
**MVP:**
- [ ] Leaflet/MapLibre base + estructura capas: Alertas / Zonas / Necesidades / Ayudas (toggle)
- [ ] Consumir contratos G1 ` {id, type, lat, lon, status, direccion}` y G2 `{id, risk_level, status, zone}` vía `apiClient.js`
- [ ] Resaltar `zone` cuando `risk_level=high` (ALTO RIESGO desbloquea necesidades/ayudas)
- [ ] Marcadores + popups + intensidad 🟢🟠🔴 por conteo en zona (usa mocks si API no lista: `frontend/mocks/`)
- [ ] Interfaz principal: menú `Mapa | Alertas | Ayudas` simple

## Orden de integración (evita pisarse)
1. **P1** mergea Alertas a `dev` primero (toca `main.py`, `config.py` si hace falta — avisar)
2. **P2** y **P3** trabajan en paralelo sobre `dev` actualizado (no tocan `alertas/` ni `mapa.html`)
3. **P4** último: consume APIs de P1-P3, solo toca `mapa.html`/`mapaNecesidades.js`/`mocks`
4. Daily 15:00: `git pull --rebase origin dev` antes de push; PRs con `Closes #<num>` para Kanban

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
