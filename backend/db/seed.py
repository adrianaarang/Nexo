"""Rellena la base de datos con datos ficticios para poder hacer una
demo sin depender de un desastre real ni de integraciones ya conectadas.

Parte de la base común — cada equipo puede ampliar los datos de su
propio módulo aquí si lo necesita para probar.

Uso: python db/seed.py
"""
from database import get_cursor, init_db


def seed() -> None:
    """Reinicia las tablas de demostración e inserta datos coherentes."""

    init_db()
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM necesidades")
        cursor.execute("DELETE FROM voluntario_documentos")
        cursor.execute("DELETE FROM voluntarios")
        cursor.execute("DELETE FROM donaciones")
        cursor.execute("DELETE FROM personas")

        # Estos registros respetan el mismo contrato que usará el formulario
        # simplificado. Cubren las 8 categorías cerradas y los dos estados
        # posibles (abierta / cubierta) para poder probar filtros y mapa.
        # La "direccion" es el texto legible que en producción generaría la
        # geocodificación (ver geocodificacion.js); aquí se escribe a mano
        # porque son coordenadas de ejemplo, no una búsqueda real.
        cursor.executemany(
            """INSERT INTO necesidades
               (titulo, tipo, descripcion, direccion, latitud, longitud, prioridad, estado)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    "Agua potable",
                    "agua",
                    "Punto sin agua potable desde hace 2 días",
                    "Carrer de la Pau 12, Valencia",
                    39.4699,
                    -0.3763,
                    "alta",
                    "abierta",
                ),
                (
                    "Alojamiento temporal",
                    "refugio",
                    "Familia de 4 sin techo, necesita alojamiento temporal",
                    "Plaza del Ayuntamiento, Valencia",
                    39.4712,
                    -0.3801,
                    "alta",
                    "abierta",
                ),
                (
                    "Necesidad de parafarmacia",
                    "parafarmacia",
                    "Falta insulina en el centro de acogida",
                    "Calle Colón 45, Valencia",
                    39.4650,
                    -0.3750,
                    "critica",
                    "abierta",
                ),
                (
                    "Comida para 30 personas",
                    "alimentos",
                    "Reparto de comida para 30 personas",
                    "Mercado Central, Valencia",
                    39.4680,
                    -0.3720,
                    "media",
                    "cubierta",
                ),
                (
                    "Ropa de abrigo",
                    "ropa",
                    "Se necesitan abrigos y mantas para el punto de acogida",
                    "Calle Ruzafa 8, Valencia",
                    39.4665,
                    -0.3790,
                    "media",
                    "abierta",
                ),
                (
                    "Kits de higiene",
                    "higiene",
                    "Gel, compresas y pañales para el polideportivo",
                    "Polideportivo Municipal, Valencia",
                    39.4705,
                    -0.3735,
                    "media",
                    "abierta",
                ),
                (
                    "Vehículo para reparto",
                    "transporte",
                    "Furgoneta para trasladar donaciones al punto de acogida",
                    "Avenida del Puerto 30, Valencia",
                    39.4690,
                    -0.3770,
                    "baja",
                    "cubierta",
                ),
                (
                    "Necesidad de otros",
                    "otros",
                    "Material de limpieza para la zona afectada",
                    "Calle San Vicente 60, Valencia",
                    39.4675,
                    -0.3745,
                    "baja",
                    "abierta",
                ),
            ],
        )

        cursor.executemany(
            """INSERT INTO voluntarios
               (nombre, contacto, habilidades, disponibilidad, estado, disponible)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [
                (
                    "Laura Gómez",
                    "laura@example.com",
                    "sanitario, primeros auxilios",
                    "inmediata",
                    "aprobado",
                    1,
                ),
                (
                    "Marc Ferrer",
                    "marc@example.com",
                    "conductor, logística",
                    "fin de semana",
                    "aprobado",
                    1,
                ),
                (
                    "Aixa Ruiz",
                    "aixa@example.com",
                    "cocina, organización",
                    "inmediata",
                    "aprobado",
                    0,
                ),
            ],
        )

        cursor.executemany(
            """INSERT INTO donaciones (tipo, recurso, cantidad, contacto)
               VALUES (?, ?, ?, ?)""",
            [
                ("ofrecida", "Mantas", "50 unidades", "creuroja@example.com"),
                (
                    "solicitada",
                    "Agua embotellada",
                    "200 litros",
                    "puntoayuda1@example.com",
                ),
            ],
        )

        cursor.executemany(
            """INSERT INTO personas (nombre, estado, ultima_ubicacion, reportado_por)
               VALUES (?, ?, ?, ?)""",
            [
                (
                    "Josep Martí",
                    "desaparecida",
                    "Paiporta, cerca del puente",
                    "familia",
                ),
                ("Rosa Alba", "localizada", "Polideportivo municipal", "voluntario"),
            ],
        )

    print("Base de datos rellenada con datos de ejemplo.")


if __name__ == "__main__":
    seed()
