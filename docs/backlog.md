# Backlog de NEXO

> Mantenido por el Product Manager (Juan). Última actualización: 2026-08-24.
> Referencia de prioridades: `docs/manifiesto.md` y `docs/roadmap.md`.

## Estado por módulo

| Módulo | Prioridad | Rama(s) | PR | Dueño | Estado |
|--------|-----------|---------|----|-------|--------|
| Alertas oficiales | Núcleo (MVP) | `feature/alerts` | #19 **MERGED** (`1348ad7` → `feature/alerts`) | Grupo 2 (Juan, capitán) | Backend A1+A2 hechos (`get_alerts()` ~469 alertas, caché 15 min); A3/A4 (Javi) en curso; frontend `alertsApi.js`+`estadosAlertas.js` hecho. **Falta E2E (C3) + PR `feature/alerts`→`dev`** |
| Mapa de necesidades | Núcleo (MVP) | `dev` + `feature/form-cards-elenadiaz1` | #18 abierto (bloqueado) | Grupo 1 + elenadiaz1 | En curso; **riesgo de solapamiento**. Bloqueado en integración: falta GET cargar necesidades, PATCH estado (`abierta→en_proceso→cubierta`), quitar `mockNeeds`, centralizar en `necesidadesApi.js` |
| Voluntariado y donaciones | Núcleo (MVP) | `feature/donaciones-grupo3` | abierto | Grupo 3 | Solo frontend; **falta backend** donaciones (sin API definida) |
| Registro de personas / "estoy bien" | Siguiente | `feature/personas/david` | #20 abierto | Grupo 4 | PR #20 añade backend "estoy bien" (`POST /api/personas/estoy-bien`); **falta 2 aprobaciones**. BD+seed+router ya en repo; falta frontend registro |
| Modo offline (PWA) | Siguiente | — | — | Grupo 4 | Sin empezar; cola offline (`syncQueue.js`/`localDb.js`/`serviceWorker.js`) en TODO → G4 implementa |
| Documentación y gobernanza | Transversal | `feature/docs` | por abrir | PM (Juan) | Manifiesto, convenciones, reparto, backlog, `formas-de-trabajo.md`, `faq.md`, `roles-y-tareas.md` en local; actualizado 2026-08-24 tras `pull` |

## PRs en curso (2026-08-24)

> Estado tras `git pull`/`fetch`. Se incluyen los PRs revisados por el PM.

| PR | Título | Rama → destino | Estado | Revisores |
|----|--------|----------------|--------|-----------|
| #19 | fix(alertas): alinear contratos + robustecer GDACS | `juan/fix-alerts-integration` → `feature/alerts` | **MERGED** (`1348ad7`) | JCRbit, adrianaarang, jowel2701 |
| #18 | Feature/form cards (mapa E2E) | `feature/form-cards-elenadiaz1` → `dev` | Abierto, **bloqueado**: falta GET/PATCH + quitar `mockNeeds`; necesita 2 aprobaciones | Gema-Villanueva, SiR0N |
| #20 | feat(personas): add estoy bien backend | `feature/personas/david` → `dev` | Abierto; falta 2 aprobaciones | adryeli, Isabela-Tellez, Anasfady |

## Objetivos MVP (de `docs/manifiesto.md`)
- [ ] O1 Alertas GDACS con filtros y estados (núcleo del Grupo 2)
- [ ] O2 Mapa de necesidades end-to-end
- [ ] O3 Voluntariado/donaciones end-to-end
- [ ] O4 E2E completo (frontend→API→BD) con CI verde
- [ ] O5 PWA instalable con detección de conexión

## Pendientes de gobernanza (PM)
- [x] Decidir herramienta de backlog: **Trello** (1 tablero por grupo + general) — decidido
- [ ] Convocar comisión de coordinación semanal (PM + SMs + Adriana)
- [ ] Votar ADRs de decisiones cerradas (empezar por D1–D4 de Grupo 2) — `docs/adr/`
- [ ] Activar CI también en `dev` (hoy solo corre en `main`) — responsabilidad de Adriana
- [ ] README bilingüe por módulo (convenciones §19) — cada equipo en su PR
- [ ] Preparar Demo Day (narrativa alerta→mapa→necesidad→recurso→resolución)
- [ ] Revisar licencia MIT provisional académica antes de abrir código
- [ ] **1er Sprint:** prever arranque lunes/martes (confirmar fecha en comisión)
- [ ] **Tablas de datos por equipo:** cada equipo crea su tabla de prueba (voluntarios, alertas, donaciones, etc.); muestra en GitHub: usuarios, insumos, alertas
- [ ] **Formas de trabajo:** documentadas en `docs/formas-de-trabajo.md`
- [ ] **Roles y tareas:** pedir a cada Scrum Master que complete su sección en `docs/roles-y-tareas.md`

## Abierto (por decidir)
- Zonas/celdas del mapa aún no definidas.
- Alcance exacto del modo offline (decisión abierta).
- Estrategia de despliegue (solo local hoy; CI sin despliegue).

## Riesgos
- **Necesidades:** 3 personas sobre el mismo módulo → conflictos. Mitigación: dueño de archivo (conv §20) y un responsable de merge dentro del grupo.
- **Alertas:** #19 mergeado en `feature/alerts`; falta PR `feature/alerts`→`dev` para E2E completo.
- **Donaciones:** sin backend definido.
- **CI:** solo en `main`; `dev` sin protección de CI verde.
