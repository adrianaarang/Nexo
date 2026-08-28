# Datos mock — Grupo 4 (Mapa)

Datos de prueba para trabajar el mapa sin depender de que Grupo 1
(Necesidades), Grupo 2 (Alertas) y Grupo 3 (Ayudas) tengan su backend
listo. Cuando las APIs reales existan, solo hay que sustituir la fuente
de datos en `necesidadesApi.js` / `alertasApi.js` / `voluntariadoApi.js`
— la forma de los datos no debería cambiar si se respeta el contrato.

## Contrato base (acordado en la reunión del 27/08)

- **Alerta → Mapa**: `id`, `risk_level` (`low`/`medium`/`high`), `status`
  (`active`/`resolved`), `zone`.
- **Necesidad → Mapa**: `id`, `type`, `latitude`, `longitude`, `status`
  (`open`/`covered`).
- **Ayuda → Mapa**: `id`, `type`, `category`, `latitude`, `longitude`,
  `status` (`available`).

Todos los campos anteriores están tal cual en el acta. Todo lo demás
que aparece abajo es una decisión mía para poder generar datos
realistas, y debería confirmarse con el grupo correspondiente antes de
darla por definitiva.

## Decisiones tomadas (a confirmar)

- **`zone` en alertas.mock.json**: el acta deja `zone: {}` sin definir.
  Aquí se ha mockeado como GeoJSON `Polygon` (`coordinates` en
  `[longitud, latitud]`, formato estándar), porque es lo que
  `L.polygon()` de Leaflet puede consumir con menos conversión. **A
  confirmar con Grupo 2**, que es quien define el contrato real de
  alertas — si ellos devuelven otra forma (p. ej. un círculo con centro
  + radio), este mock debe cambiar antes de que Persona 2 del Grupo 4
  empiece a depender de él.

- **`type` en ayudas.mock.json**: el acta unifica donaciones y
  voluntariado bajo "Ayudas" con tres modalidades (recursos, servicios,
  tiempo) pero no cierra los valores exactos del campo. Aquí se ha usado
  `"resource"`, `"service"`, `"time"` como `type`, con `category`
  variando dentro de cada una. **A confirmar con Grupo 3**, que es quien
  define el modelo real de ayudas.

- **`created_at` en alertas.mock.json y necesidades.mock.json**: no está
  en el contrato del acta, pero es un dato importante para una app de
  emergencias — una necesidad de hace 3 días no debería priorizarse
  igual que una de hace 10 minutos. Se ha añadido como timestamp ISO
  8601 en UTC (`"2026-08-26T09:15:00Z"`). **A confirmar con Grupo 1 y
  Grupo 2**: si el backend no devuelve este campo, Persona 4 (mostrar
  peticiones/ayudas) no podrá ordenar ni destacar por antigüedad. No se
  ha añadido a ayudas.mock.json por ahora — solo se pidió para alertas
  y necesidades.

- **Sin DNI ni nombre en el voluntariado del mapa**: el acta pide DNI y
  nombre al registrar un voluntariado, pero `docs/privacidad-datos.md`
  del propio repo dice que no se debe pedir más dato del necesario y
  que el MVP no tiene login (todo lo que devuelva la API es público).
  Por eso este mock no incluye datos personales — esos campos, si
  existen, deberían quedarse en el backend de Grupo 3 y no salir en la
  respuesta que consume el mapa.

## Categorías usadas en necesidades.mock.json

`water`, `food`, `medication`, `clothing`, `hygiene`, `shelter`,
`transport` — mapeadas de las categorías cerradas del acta (Agua,
Alimentos, Medicamentos, Ropa, Higiene, Refugio, Transporte, Otros).
