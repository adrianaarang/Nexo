# Registro — Estado de PRs y sincronización (24/08/2026)

**Responsable:** Product Manager (Juan).
**Contexto:** revisión de estado tras `git pull`/`fetch` y preparación de Sprint 2.

## Acciones realizadas
1. `git fetch --all --prune`: `feature/alerts` avanzó `34359fe..1348ad7`; nueva rama `feature/personas/david` (PR #20).
2. Confirmado merge de **PR #19** (`juan/fix-alerts-integration` → `feature/alerts`, commit `1348ad7`): se alinearon contratos del proyecto ( `crearTarjeta`, `alertas.html`, `get_alerts`) y se robusteció el parser GDACS + cliente Protección Civil. Rama de PR borrada tras merge.
3. Actualizado `docs/backlog.md` con trazabilidad de PRs (#18, #19, #20) y estado por módulo.

## Estado de PRs
- **#19 — Alertas:** MERGED en `feature/alerts`. Falta PR `feature/alerts`→`dev` para E2E.
- **#18 — Mapa (form cards):** abierto y bloqueado en integración. Pendiente: GET cargar necesidades, PATCH estado (`abierta→en_proceso→cubierta`), quitar `mockNeeds`, centralizar en `necesidadesApi.js`. Revisores: Gema-Villanueva, SiR0N.
- **#20 — Personas "estoy bien":** abierto. Backend `POST /api/personas/estoy-bien` implementado (45 tests verdes). Falta 2 aprobaciones. Revisores: adryeli, Isabela-Tellez, Anasfady.

## Notas
- `feature/docs` es rama local (sin remoto); los cambios de documentación se registrarán aquí y se abrirá PR cuando el PM lo indique.
- Riesgo de solapamiento en mapa (varias personas sobre el mismo módulo) sigue vigente.
