# Privacidad y tratamiento de datos (borrador)

Nexo maneja dos tipos de datos especialmente sensibles: ubicación en tiempo
real (mapa de necesidades) y datos de personas desaparecidas/localizadas. Este
documento recoge los criterios mínimos a seguir, pendiente de revisión legal
antes de cualquier despliegue real.

- **Minimización**: no se pide más dato del necesario para que la ayuda llegue
  (por ejemplo, no se pide DNI para registrar una necesidad).
- **Consentimiento**: registrar a otra persona como desaparecida/localizada
  debería dejar constancia de quién lo reporta (`reportado_por`), para poder
  corregir o retirar el dato si la propia persona lo pide.
- **Retención limitada**: los datos de una emergencia concreta no deberían
  guardarse indefinidamente una vez resuelta — pendiente de definir un plazo.
- **Acceso**: en el MVP no hay login (para no añadir fricción en una
  emergencia), lo que significa que cualquiera puede ver los datos expuestos
  por la API. Antes de un despliegue real hay que decidir qué datos son
  públicos (necesidades, alertas) y cuáles deberían restringirse (datos de
  contacto de personas desaparecidas, por ejemplo).
- **GDACS y Protección Civil**: solo se consumen datos públicos de estas
  fuentes, no se les envía ningún dato de usuarios de Nexo.

Este documento es un punto de partida para la evaluación académica, no un
análisis legal completo.
