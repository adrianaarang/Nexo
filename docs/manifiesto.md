# Manifiesto de NEXO

*"Conectados para ayudarnos — respuesta a emergencias y desastres."*

- **Versión:** 1.0 — 2026-08-20
- **Marco de referencia**
- **Autor:** Juan (Product Manager)
- **Colaboradores:** Adriana, SMs y jefes de equipo
- **Paige de decisión:** Juan (PM) · `docs/manifiesto.md`

## 1. Resumen ejecutivo
NEXO es una PWA de coordinación de respuesta a emergencias: integra alertas oficiales
mundiales (GDACS) con un mapa de necesidades en tiempo real y conecta voluntarios y
donaciones con quien las necesita. Actúa como **infraestructura de coordinación**, no como
red social.

## 2. Misión
Para personas/comunidades afectadas que no saben qué se necesita ni cómo ayudar, NEXO es
una web de coordinación en tiempo real (alertas + mapa + voluntarios/donaciones), sin login,
mobile-first, donde cualquiera ve el panorama y ayuda o pide ayuda en un clic.

## 3. Visión
Convertir información dispersa y respuesta desorganizada en capacidad coordinada. A medio
plazo, ser la capa abierta de coordinación ("Resilience API / Climate OS").

## 4. Principios no negociables
1. **Emergencia pura** — respuesta inmediata, no red social.
2. **Evidencia y fuentes oficiales** — GDACS; datos ciudadanos complementan, no sustituyen.
3. **Coordinación antes que predicción** — el MVP resuelve la respuesta; IA es horizonte posterior.
4. **Accesibilidad y baja fricción** — sin login, mobile-first, siempre estados carga/vacío/error.
5. **Privacidad por diseño** — minimización, consentimiento, retención limitada.
6. **Equidad** — prioriza poblaciones vulnerables, no solo números.
7. **Abierto y reproducible** — arquitectura modular, documentada, código abierto a futuro.
8. **El LLM explica, no decide** (si llega el horizonte de IA).

## 5. Objetivos del MVP (criterios de éxito)
| # | Objetivo | Criterio de éxito |
|---|----------|-------------------|
| O1 | Alertas oficiales mundiales (GDACS) con filtros tipo/severidad/país y estados carga/vacío/error | Ver alertas reales o simuladas sin que una caída de GDACS rompa la pantalla (nunca 500) |
| O2 | Mapa de necesidades en tiempo real (crear, listar, cambiar estado) | Un usuario publica una necesidad y aparece en el mapa; otra la marca cubierta |
| O3 | Voluntariado y donaciones: ofrecer/solicitar y marcar cubierto/asignado | Se publica una oferta, se asigna y deja de pedirse lo ya cubierto |
| O4 | End-to-end completo (frontend → API → BD) con CI en verde | Los 4 equipos integran su pantalla en el recorrido común sin romper nada |
| O5 | PWA instalable con detección de conexión | Se instala desde el móvil y muestra estado de conexión (offline real es siguiente fase) |

**Historia demo:** alerta → mapa → necesidad → recurso/voluntario → resolución.

## 6. Qué NO es NEXO (fuera de alcance)
- No predice desastres (los consume de fuentes oficiales).
- No es red social ni marketplace.
- No emite alertas ni sustituyen a Protección Civil / AEMET (hueco TODO documentado).
- El LLM no decide protocolos.
- No acumula datos personales de más; sin login en el MVP.

## 7. Alcance por horizontes
| Horizonte | Contenido | Equipo(s) |
|-----------|-----------|-----------|
| Núcleo / MVP (demo) | Mapa de necesidades · Alertas oficiales · Voluntariado y donaciones · Base común | E1, E2, E3 + Integradora |
| Siguiente prioridad | Personas (desaparecidas / estoy bien) · Modo offline real (IndexedDB + cola + sync) | E4 |
| Futuro ("Sin fin del mundo" / Resilience OS) | Simulador, what-if, índice de resiliencia, puntos de fallo, presupuesto, stress tests, equidad, agente que explica, Resilience API | A definir |

## 8. Organización del proyecto
| Rol | Persona | Responsabilidad principal |
|-----|---------|---------------------------|
| Product Manager | **Juan** | Alcance, priorización, **backlog**, gobernanza, comunicación |
| Scrum Masters por equipo | Josema · Laura S.R. · Isabela Téllez · Juan | Proceso, bloqueos, dailies/retros |
| Integradora / repo owner | **Adriana** | Base común, **integración, CI, PRs, demo global** |
| Equipo 1 / 2 / 3 / 4 | Necesidades · Alertas · Ayudas · Mapa/Interfaz | Vertical completa de su módulo (frontend + backend) |

**Gobernanza:** comisión de coordinación semanal (PM + SMs + Integradora); lo estratégico en
asamblea. Marco: convenciones del proyecto (idioma técnico en inglés / UI en español).

## 9. Marco de trabajo del MVP
Sprint semanal, daily 15 min, refinado, demo al cierre, retrospectiva.
- **Ready:** objetivo claro · responsable · criterios de aceptación · tamaño razonable.
- **Done:** implementado · sigue arquitectura · pytest verde · integrado · revisado · demostrable.
- **Calidad:** CI verde antes del merge (pendiente: activarlo en `dev`), tests por módulo, fuentes externas mockeadas.

## 10. Criterios de éxito del proyecto
1. Recorrido demo completo e integrado en local.
2. Los 4 equipos presentan su módulo end-to-end.
3. Código limpio según convenciones, CI verde, sin pantallas en blanco.
4. Documentación coherente con la realidad del código.
5. Retrospectiva con aprendizajes y propuesta de siguiente fase.

## 11. Riesgos críticos
| Riesgo | Mitigación |
|--------|------------|
| GDACS vacío/caído en demo | Caché 15 min + datos simulados de reserva |
| Solapamiento entre equipos | Propiedad de archivos y aviso antes de tocar ajeno |
| Verticales incompletas | Un módulo end-to-end por equipo + integración continua |
| CI roto o sin cubrir `dev` | Tests mínimos + activar CI en `dev` |
| Alcance que crece a mitad de sprint | "No more features": todo cambio pasa por el backlog |

## 12. Ética y licencia
Prioridades considerando vulnerabilidad, no solo números. Licencia MIT provisional académica
(revisar antes de abrir). Este manifiesto es la referencia de alcance y decisiones de producto.
