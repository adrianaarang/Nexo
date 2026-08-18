# Nexo — Estructura explicada

## Raíz del proyecto

- **README.md** — qué es Nexo, cómo instalarlo y arrancarlo. Lo primero que lee cualquiera que abra el repo.
- **LICENSE** — licencia de código abierto (fase futura, cuando el proyecto se abra a colaboración externa).
- **CONTRIBUTING.md** — normas para que otras personas puedan aportar código (futuro).
- **.gitignore** — qué archivos no debe subir git (node_modules, .env, bases de datos locales...).
- **.env.example** — plantilla de variables de entorno (claves de API, URLs) sin datos reales, para que cada persona cree su propio `.env`.
- **.github/workflows/ci.yml** — automatiza que, cada vez que alguien sube código, se ejecuten tests y comprobaciones básicas antes de aceptar el cambio.

## `frontend/` — interfaz de usuario (HTML/CSS/JS)

- **index.html** — la pantalla de entrada de la app; carga el mapa de necesidades, que es el módulo más votado.
- **manifest.json** — convierte la web en PWA (app instalable), pieza clave para que el modo offline funcione.
- **pages/** — una página HTML por pantalla principal: mapa, alertas, voluntariado, donaciones, personas y "estoy bien". Separarlas facilita que cada persona del equipo trabaje en una sin pisar el código de otra.
- **css/variables.css** — colores y tipografía de marca de Nexo en un solo sitio, para no repetir valores por todo el proyecto.
- **css/style.css** — estilos generales (layout, espaciados).
- **css/components.css** — estilos de piezas reutilizables (tarjetas, botones, cabecera).
- **js/app.js** — arranca la app y decide qué página mostrar (router simple sin framework).

### `js/core/` — módulos del MVP (los que ganaron la encuesta)
- **mapa-necesidades/mapaNecesidades.js** — lógica de la pantalla del mapa.
- **mapa-necesidades/necesidadCard.js** — la tarjeta que muestra cada necesidad (agua, comida, refugio...) sobre el mapa.
- **mapa-necesidades/necesidadesApi.js** — llamadas al backend para leer/crear necesidades.
- **alertas-oficiales/alertas.js** — muestra las alertas activas al usuario.
- **alertas-oficiales/alertasApi.js** — pide al backend las alertas (que vienen de GDACS/Protección Civil).
- **voluntariado-donaciones/voluntariado.js** — pantalla para apuntarse como voluntario.
- **voluntariado-donaciones/donaciones.js** — pantalla para ofrecer o pedir donaciones.
- **voluntariado-donaciones/voluntariadoApi.js** — llamadas al backend de este módulo.

### `js/siguiente/` — siguientes prioridades
- **registro-personas/registroPersonas.js** — formulario para registrar a alguien como desaparecido o localizado.
- **registro-personas/estoyBien.js** — botón rápido de "estoy bien" para marcar el propio estado.
- **registro-personas/personasApi.js** — llamadas al backend de este módulo.
- **modo-offline/localDb.js** — guarda datos en el propio dispositivo (IndexedDB) cuando no hay conexión.
- **modo-offline/syncQueue.js** — guarda en cola las acciones hechas sin red, para enviarlas al backend en cuanto vuelva la conexión.
- **modo-offline/serviceWorker.js** — el script que permite que la app siga funcionando (parcialmente) sin internet.

### `js/futuro/` — roadmap, no se construye todavía
- **red-mesh-satelite/README.md** — notas de cómo se conectaría la app sin internet a través de redes mesh o satélite, para cuando llegue esa fase.
- **codigo-abierto/README.md** — notas sobre cómo abrir el proyecto a la comunidad más adelante.

### `js/shared/` — código común a toda la app
- **apiClient.js** — un único punto por el que pasan todas las peticiones al backend; facilita interceptar peticiones y encolarlas si no hay red.
- **utils.js** — funciones pequeñas reutilizables (formatear fechas, validar formularios...).
- **components/header.js** — cabecera común a todas las páginas.
- **components/card.js** — tarjeta genérica reutilizada por varios módulos.

### `assets/`
- **logo/** — el logo de Nexo en distintos tamaños.
- **icons/** — iconos de la interfaz.
- **images/** — imágenes generales de la app.

## `backend/` — servidor (Python)

- **requirements.txt** — lista de librerías Python que necesita el proyecto.
- **main.py** — el punto de arranque del servidor (FastAPI).
- **config.py** — configuración general (puertos, claves, entorno).
- **.env.example** — igual que en la raíz, plantilla de variables de entorno del backend.

### `modules/` — un módulo por funcionalidad, cada uno con sus propias rutas, modelos y validaciones
- **necesidades/routes.py** — endpoints para crear/leer/actualizar necesidades sobre el mapa.
- **necesidades/models.py** — cómo se guarda una "necesidad" en la base de datos.
- **necesidades/schemas.py** — qué forma deben tener los datos que entran y salen de la API.
- **alertas/routes.py** — endpoint que la app consulta para pedir alertas activas.
- **alertas/services.py** — lógica que llama a `integrations/gdacs_client.py` y traduce esos datos al formato de Nexo.
- **voluntariado/** (routes, models, schemas) — igual que necesidades, pero para altas de voluntarios.
- **donaciones/** (routes, models) — igual, para donaciones ofrecidas/solicitadas.
- **personas/** (routes, models, schemas) — registro de personas desaparecidas/localizadas y estado "estoy bien".

### `integrations/` — conexión con fuentes externas
- **gdacs_client.py** — pide alertas de desastres a nivel mundial al sistema GDACS (ONU/Comisión Europea). Es la fuente principal del módulo de alertas.
- **proteccion_civil_client.py** — capa opcional para traer detalle más fino dentro de España, complementando a GDACS.

### `sync/`
- **sync_controller.py** — recibe las acciones que el frontend guardó offline y las aplica en la base de datos, resolviendo qué hacer si hay conflictos (por ejemplo, dos personas editando la misma necesidad).

### `middleware/`
- **auth.py** — comprueba quién puede hacer qué (por ejemplo, evitar que cualquiera borre datos de otros usuarios).
- **error_handler.py** — centraliza cómo se devuelven los errores al frontend, para que sean consistentes.

### `db/`
- **database.py** — configura la conexión a la base de datos.
- **migrations/001_init.sql** — crea las tablas iniciales (necesidades, alertas, voluntarios, donaciones, personas).
- **seed.py** — rellena la base de datos con datos ficticios, para poder hacer una demo sin depender de un desastre real.

## `infra/mesh-satelite/` — futuro, solo documentación por ahora
- **README.md** y **notas-tecnicas.md** — apuntes de cómo se abordaría la conectividad sin internet cuando el proyecto llegue a esa fase; no hay código todavía porque no es parte del MVP.

## `tests/`
- **frontend/mapa-necesidades.test.js** — comprueba que el módulo más importante del frontend funciona como se espera.
- **backend/test_necesidades.py** — mismo tipo de comprobación, pero sobre la API del backend.

## `docs/`
- **decisiones-encuesta.md** — resumen de los resultados de la encuesta del grupo y por qué se eligió este alcance (para poder justificarlo en la presentación o evaluación).
- **roadmap.md** — qué es núcleo, qué es siguiente prioridad y qué es futuro, explicado para cualquiera que se una al proyecto.
- **architecture.md** — cómo encajan frontend y backend entre sí.
- **privacidad-datos.md** — cómo se trata la ubicación en tiempo real y los datos de personas desaparecidas, que son datos sensibles.
