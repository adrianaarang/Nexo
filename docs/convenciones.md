# Convenciones del proyecto NEXO

**v0.8** · 24 puntos a votar · Documento vivo

Cada decisión se cierra en la comisión de coordinación (4 jefes + PO + SM) y queda registrada
como ADR (`docs/adr/NNN-nombre.md`). Hasta que se vote, se aplica la propuesta profesional salvo
objeción expresa del grupo; ante un choque, se avisa en la daily antes de improvisar.

## A. Puntos a definir (propuestas profesionales)

| # | Tema | Propuesta |
|---|------|-----------|
| 1 | Idioma | Commits y mensajes de Git en inglés. Comentarios indistintamente en inglés o castellano (respeta el archivo que tocas). README bilingüe. **Textos de UI en español. Docs técnicos en español.** El español en identificadores (ej. `obtenerAlertas`) se migra a inglés en refactor post-demo |
| 2 | Naming | Python `snake_case` (`get_alerts`). JS `camelCase`, función = verbo (`getAlerts`). Constantes `SNAKE_CASE` (`GDACS_CACHE_TTL_SECONDS`). Clases `PascalCase`. Tablas SQL `snake_case`. Booleans `is_`/`has_`. CSS `nexo-` + BEM-lite. Respetar lo ya usado en el archivo |
| 3 | Ramas | `feature/<modulo>` (grupo) y `feature/<modulo>/<nombre>` (personal). `dev` integra, `main` solo lo de la demo. **Siempre `pull` antes de `push`** (reunión jefes 21/08). Opción A: rama propia por persona para probar y luego subir a `dev`; opción B: rama por tarea que se sube a `dev` |
| 4 | Commits | Conventional Commits en inglés: `feat(alertas): add GDACS client`. Sin "wip". Un tema por commit |
| 5 | Protección de ramas | Sí, proteger `dev` y `main` (lo habilita Adriana) |
| 6 | PRs y revisión | Mínimo 1 revisor del grupo + aprobación del **capitán**; el capitán mergea; **CI obligatoriamente en verde** |
| 7 | Backend | Módulo = `backend/modules/<modulo>/` (routes, models, schemas, services). REST en `/api/<modulo>`. Errores con formato único `{"error","detalle"}`. Integraciones externas en `backend/integrations/` con caché; fallo de fuente → `[]` con 200, nunca 500. Sin dependencias nuevas sin justificar. `config.py` + `.env.example` |
| 8 | Frontend | Vanilla JS, ES modules, sin framework. Base común obligatoria: `apiGet/apiPost`, `formatDate`, `el`, `crearTarjeta`. CSS con variables `nexo-`; estilos de pantalla en `css/<pantalla>.css`. 1 pantalla = 1 módulo JS |
| 9 | Base de datos | Migraciones nuevas `NNN_nombre.sql`, idempotentes, sin tocar las ajenas. Seed solo en `db/seed.py` |
| 10 | Contratos entre módulos | Cada módulo documenta su contrato en `docs/` y `schemas.py`; los frontend consumen el contrato sin inventar campos; cambios se anuncian en la daily |
| 11 | Testing / CI | Backend: `pytest` por módulo con fuentes externas mockeadas. Frontend: `tests/frontend/<modulo>.test.js`. CI en todo push/PR, verde |
| 12 | Gestión de trabajo | Trello por grupo + Trello general (acordado). Issues de GitHub opcionales con etiqueta por grupo. Dailies de 15 min para bloqueos |
| 13 | Ready / Done | Ver secciones C y D |
| 14 | Demo Day | Recorrido narrativo alerta → mapa → necesidad → recurso/voluntario → resolución. Datos simulados de reserva si GDACS no tiene eventos |
| 15 | ADR | `docs/adr/NNN-nombre.md`, uno por decisión, votado en comisión |
| 16 | Reglas duras | Ver sección B (6 reglas) |
| 17 | Setup local | Backend: venv + `pip install -r requirements.txt` con versiones fijadas. Puerto 8000. Si no corre en tu máquina: parar y avisar, no seguir a ciegas |
| 18 | Seguridad mínima | Validar toda entrada de usuario en la API; nunca hardcodear claves; sanitizar texto en UI; CORS solo al origen del front. Amplía la regla dura 1 |
| 19 | Documentación de módulos | Cada módulo lleva un README.md bilingüe corto (qué hace, cómo probarlo, contrato de datos). Referencia obligatoria en el PR |
| 20 | Propiedad de archivos | Lista de dueños por archivo; avisar antes de tocar archivo ajeno (regla dura 3); conflictos en PR los resuelve el dueño del archivo |
| 21 | Integrador rotativo | Una persona por iteración (rotatorio) mergea `feature/*` → `dev` y avisa de roturas; el capitán valida su módulo |
| 22 | Mobile-first / accesibilidad | Diseñar desde móvil (≥360px), contraste AA, textos legibles, y estados carga/vacío/error en TODA pantalla (nunca pantallas en blanco) |
| 23 | Planificación e hitos (opc) | Sprint semanal (lun-vie) con entrega esperada por grupo; la demo es el hito final |
| 24 | Checklist de revisión PR (opc) | Revisar también estados carga/vacío/error, formato de datos reales y que la UI no rompa en móvil |

## B. Reglas duras (sí o sí)
1. No commitear `.env`/claves/tokens.
2. No tocar archivos ajenos: `main.py`, migraciones de otros, `apiClient.js`, CSS compartidos.
3. No renombrar/borrar archivos existentes sin avisar al dueño.
4. No añadir dependencias sin justificar y avisar.
5. No mergear con CI en rojo.
6. No commits directos en `dev`/`main`.

## C. Criterios de tarea
- **Ready:** objetivo claro · responsable · contexto · criterios de aceptación · tamaño razonable.
- **Done:** implementado · sigue la arquitectura · pytest verde · integrado en el recorrido completo · revisado y mergeado · demostrable.

## D. Cierre
Se vota tema por tema en la comisión; cada acuerdo se registra como ADR y actualiza este documento.
