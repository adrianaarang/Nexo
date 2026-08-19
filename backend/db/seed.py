"""Rellena la base de datos con datos ficticios para poder hacer una
demo sin depender de un desastre real ni de integraciones ya conectadas.

Parte de la base común — cada equipo puede ampliar los datos de su
propio módulo aquí si lo necesita para probar.

Uso: python db/seed.py
"""
from database import get_cursor, init_db


def seed():
    init_db()
    with get_cursor() as cur:
        cur.execute("DELETE FROM necesidades")
        cur.execute("DELETE FROM voluntarios")
        cur.execute("DELETE FROM donaciones")
        cur.execute("DELETE FROM personas")

        cur.executemany(
            """INSERT INTO necesidades (tipo, descripcion, latitud, longitud, prioridad, estado)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [
                ("agua", "Punto sin agua potable desde hace 2 días", 39.4699, -0.3763, "alta", "abierta"),
                ("refugio", "Familia de 4 sin techo, necesita alojamiento temporal", 39.4712, -0.3801, "alta", "abierta"),
                ("medicinas", "Falta insulina en el centro de acogida", 39.4650, -0.3750, "alta", "en_proceso"),
                ("comida", "Reparto de comida para 30 personas", 39.4680, -0.3720, "media", "cubierta"),
            ],
        )

        cur.executemany(
            """INSERT INTO voluntarios (nombre, contacto, habilidades, disponibilidad)
               VALUES (?, ?, ?, ?)""",
            [
                ("Laura Gómez", "laura@example.com", "sanitario, primeros auxilios", "inmediata"),
                ("Marc Ferrer", "marc@example.com", "conductor, logística", "fin de semana"),
                ("Aixa Ruiz", "aixa@example.com", "cocina, organización", "inmediata"),
            ],
        )

        cur.executemany(
            """INSERT INTO donaciones (tipo, recurso, cantidad, contacto)
               VALUES (?, ?, ?, ?)""",
            [
                ("ofrecida", "Mantas", "50 unidades", "creuroja@example.com"),
                ("solicitada", "Agua embotellada", "200 litros", "puntoayuda1@example.com"),
            ],
        )

        cur.executemany(
            """INSERT INTO personas (nombre, estado, ultima_ubicacion, reportado_por)
               VALUES (?, ?, ?, ?)""",
            [
                ("Josep Martí", "desaparecida", "Paiporta, cerca del puente", "familia"),
                ("Rosa Alba", "localizada", "Polideportivo municipal", "voluntario"),
            ],
        )

    print("Base de datos rellenada con datos de ejemplo.")


if __name__ == "__main__":
    seed()
