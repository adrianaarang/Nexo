# Contrato API: voluntariado

Base URL: `/api`. Los nombres de campos JSON son `snake_case` y los booleanos empiezan por `is_`.

## Voluntarios

`POST /volunteers` recibe y devuelve un voluntario:

```json
{
  "id": "uuid",
  "first_name": "Ana",
  "last_name": "Pérez",
  "dni": "12345678Z",
  "birth_date": "1995-05-14",
  "phone": "+34 600 000 000",
  "locality": "Valencia",
  "tasks": ["supply_distribution", "telephone_information"],
  "certifications": ["first_aid", "driving_license_b"],
  "transportation": "own_vehicle",
  "vehicle_type": "car",
  "availability_slots": [{ "starts_at": "2026-08-24T08:00:00" }],
  "skills": "vehículo propio",
  "status": "available"
}
```

`first_name` y `last_name` admiten nombres compuestos, letras y signos de puntuación. `dni` debe tener ocho números y la letra de control correcta, sin espacios. `locality` indica dónde puede ayudar la persona. `tasks` y `certifications` son listas de los valores del formulario; `tasks` debe contener al menos un elemento. `transportation` admite `own_vehicle` o `needs_transport`; `vehicle_type` es `car`, `van`, `four_by_four` o `null`. `availability_slots` contiene cada hora marcada por la persona. `status` admite `available`, `assigned` o `resting`; al registrarse siempre es `available`.

`GET /voluntarios?status={status}` devuelve voluntarios, filtrados opcionalmente por estado, sin incluir el teléfono. `PATCH /voluntarios/{volunteer_id}` recibe `{ "status": "available|assigned|resting" }`. Este cambio debe estar autorizado solo para coordinación, especialmente la transición a `assigned`.

## Donaciones (contrato para su módulo propietario)

La pantalla de voluntariado no lee ni modifica donaciones. Para que el módulo de donaciones pueda aplicar la regla acordada, su `GET /donations` debe devolver:

```json
{
  "id": "uuid",
  "id": "uuid",
  "title": "Agua embotellada",
  "esta_cubierta": false
}
```

Cuando `esta_cubierta` sea `true`, su frontend añade una clase gris, muestra “Necesidad cubierta” y deshabilita la acción de donar. La transición debe validarse en el backend del módulo de donaciones.
