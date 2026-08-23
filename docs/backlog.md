# Backlog de NEXO

> Mantenido por el Product Manager (Juan). Última actualización: 2026-08-23.
> Referencia de prioridades: `docs/manifiesto.md` y `docs/roadmap.md`.

## Estado por módulo

| Módulo | Prioridad | Rama(s) | PR | Dueño | Estado |
|--------|-----------|---------|----|-------|--------|
| Alertas oficiales | Núcleo (MVP) | `feature/alerts` (backend) + `juan/alerts-frontend` (frontend) | por abrir | Grupo 2 (Juan, capitán) | Backend + frontend listos y con contrato alineado; **falta merge a `dev` + E2E** |
| Mapa de necesidades | Núcleo (MVP) | `dev` (grupo1) + `feature/necesidades/gema` + `feature/form-cards-elenadiaz1` | abierto | Grupo 1 + gema + elenadiaz1 | En curso; **riesgo de solapamiento** (3 personas sobre lo mismo) |
| Voluntariado y donaciones | Núcleo (MVP) | `feature/donaciones-grupo3` | abierto | Grupo 3 | Solo frontend; **falta backend** |
| Registro de personas / "estoy bien" | Siguiente | `juan/alerts-frontend` (`registro-personas/`) | — | Grupo 4 | Borrador en rama local; sin backend ni PR |
| Modo offline (PWA) | Siguiente | — | — | Grupo 4 | Sin empezar |
| Documentación y gobernanza | Transversal | `feature/docs` | por abrir | PM (Juan) | Manifiesto, convenciones, reparto y backlog añadidos en local |

## Objetivos MVP (de `docs/manifiesto.md`)
- [ ] O1 Alertas GDACS con filtros y estados (núcleo del Grupo 2)
- [ ] O2 Mapa de necesidades end-to-end
- [ ] O3 Voluntariado/donaciones end-to-end
- [ ] O4 E2E completo (frontend→API→BD) con CI verde
- [ ] O5 PWA instalable con detección de conexión

## Pendientes de gobernanza (PM)
- [ ] Convocar comisión de coordinación semanal (PM + SMs + Adriana)
- [ ] Votar ADRs de decisiones cerradas (empezar por D1–D4 de Grupo 2) — `docs/adr/`
- [ ] Activar CI también en `dev` (hoy solo corre en `main`) — responsabilidad de Adriana
- [ ] Decidir herramienta de backlog (Trello por grupo + general, según convenciones §12)
- [ ] README bilingüe por módulo (convenciones §19) — cada equipo en su PR
- [ ] Preparar Demo Day (narrativa alerta→mapa→necesidad→recurso→resolución)
- [ ] Revisar licencia MIT provisional académica antes de abrir código

## Riesgos
- **Necesidades:** 3 personas sobre el mismo módulo → conflictos. Mitigación: dueño de archivo (conv §20) y un responsable de merge dentro del grupo.
- **Alertas:** fuera de `dev` hasta integrarse → no hay E2E.
- **Donaciones:** sin backend definido.
- **CI:** solo en `main`; `dev` sin protección de CI verde.
