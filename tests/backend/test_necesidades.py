"""Pruebas unitarias de modelos y validaciones de necesidades."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pydantic import ValidationError

from db import database
from modules.necesidades.models import (
    TransicionEstadoInvalida,
    actualizar_estado_necesidad,
    crear_necesidad,
    listar_necesidades,
    obtener_necesidad,
)
from modules.necesidades.schemas import (
    EstadoNecesidad,
    NecesidadActualizarEstado,
    NecesidadCrear,
    NecesidadRespuesta,
    TipoNecesidad,
)


class TestNecesidades(unittest.TestCase):
    """Comprueba el contrato del módulo usando una SQLite aislada."""

    def setUp(self):
        """Crea una base nueva antes de cada prueba para evitar contaminación."""

        self.directorio_temporal = TemporaryDirectory()
        self.ruta_anterior = database.DATABASE_PATH
        database.DATABASE_PATH = str(
            Path(self.directorio_temporal.name) / "nexo_test.db"
        )
        database.init_db()

    def tearDown(self):
        """Restaura la configuración y elimina la base temporal."""

        database.DATABASE_PATH = self.ruta_anterior
        self.directorio_temporal.cleanup()

    @staticmethod
    def crear_datos_validos(**cambios):
        """Genera una entrada válida y permite variar solo el campo probado."""

        datos = {
            "titulo": "Agua potable y mantas",
            "tipo": "agua",
            "descripcion": "Se necesita agua potable",
            "latitud": 39.4699,
            "longitud": -0.3763,
        }
        datos.update(cambios)
        return NecesidadCrear(**datos)

    def test_crear_y_leer_necesidad_con_valores_normalizados(self):
        """La creación devuelve una fila completa que después puede leerse."""

        necesidad = self.crear_datos_validos(
            descripcion="  Agua para el refugio  "
        )

        creada = crear_necesidad(necesidad)

        self.assertEqual(creada, obtener_necesidad(creada["id"]))
        self.assertEqual(creada["titulo"], "Agua potable y mantas")
        self.assertEqual(creada["descripcion"], "Agua para el refugio")
        self.assertEqual(creada["prioridad"], "media")
        self.assertEqual(creada["estado"], "abierta")
        # La fila también debe cumplir el contrato público de respuesta.
        respuesta = NecesidadRespuesta.model_validate(creada)
        self.assertEqual(respuesta.id, creada["id"])

    def test_registro_cumple_el_contrato_de_datos_completo(self):
        """El ejemplo compartido se guarda y serializa sin cambiar su forma."""

        creada = crear_necesidad(
            NecesidadCrear(
                titulo="Agua potable y mantas",
                tipo="agua",
                descripcion=(
                    "Se necesitan 50L de agua en el punto de recogida del barrio"
                ),
                latitud=36.463,
                longitud=-6.195,
                prioridad="alta",
            )
        )

        respuesta = NecesidadRespuesta.model_validate(creada).model_dump(
            mode="json"
        )

        self.assertIsInstance(respuesta["id"], int)
        self.assertEqual(respuesta["titulo"], "Agua potable y mantas")
        self.assertEqual(respuesta["tipo"], "agua")
        self.assertEqual(respuesta["prioridad"], "alta")
        self.assertEqual(respuesta["estado"], "abierta")
        self.assertTrue(respuesta["creado_en"].endswith("Z"))

    def test_listar_necesidades_permite_filtrar_por_estado_y_tipo(self):
        """Los filtros devuelven solo las filas que coinciden con ambos enums."""

        agua = crear_necesidad(self.crear_datos_validos())
        crear_necesidad(
            self.crear_datos_validos(
                titulo="Comida caliente",
                tipo="alimento",
                descripcion="Comida caliente",
            )
        )
        actualizar_estado_necesidad(agua["id"], EstadoNecesidad.EN_PROCESO)
        actualizar_estado_necesidad(agua["id"], EstadoNecesidad.CUBIERTA)

        cubiertas = listar_necesidades(estado=EstadoNecesidad.CUBIERTA)
        comida = listar_necesidades(tipo=TipoNecesidad.ALIMENTO)

        self.assertEqual([fila["id"] for fila in cubiertas], [agua["id"]])
        self.assertEqual([fila["tipo"] for fila in comida], ["alimento"])

    def test_actualizar_estado_devuelve_el_registro_actualizado(self):
        """Un avance válido devuelve inmediatamente el estado persistido."""

        creada = crear_necesidad(self.crear_datos_validos())

        actualizada = actualizar_estado_necesidad(
            creada["id"],
            EstadoNecesidad.EN_PROCESO,
        )

        self.assertEqual(actualizada["estado"], "en_proceso")

    def test_operaciones_sobre_id_inexistente_devuelven_none(self):
        """La capa de rutas podrá convertir la ausencia del id en HTTP 404."""

        self.assertIsNone(obtener_necesidad(999))
        self.assertIsNone(
            actualizar_estado_necesidad(999, EstadoNecesidad.CUBIERTA)
        )

    def test_estado_solo_avanza_en_el_orden_acordado(self):
        """No se permiten saltos, reaperturas ni retrocesos de estado."""

        creada = crear_necesidad(self.crear_datos_validos())

        with self.assertRaises(TransicionEstadoInvalida):
            actualizar_estado_necesidad(
                creada["id"],
                EstadoNecesidad.CUBIERTA,
            )

        en_proceso = actualizar_estado_necesidad(
            creada["id"],
            EstadoNecesidad.EN_PROCESO,
        )
        repetida = actualizar_estado_necesidad(
            creada["id"],
            EstadoNecesidad.EN_PROCESO,
        )
        self.assertEqual(en_proceso, repetida)

        actualizar_estado_necesidad(creada["id"], EstadoNecesidad.CUBIERTA)
        with self.assertRaises(TransicionEstadoInvalida):
            actualizar_estado_necesidad(
                creada["id"],
                EstadoNecesidad.ABIERTA,
            )

    def test_creacion_rechaza_campos_invalidos(self):
        """Los límites y enums rechazan datos fuera del contrato."""

        casos = [
            ("tipo", "combustible"),
            ("titulo", "  "),
            ("descripcion", "  "),
            ("latitud", 90.1),
            ("longitud", -180.1),
            ("latitud", float("nan")),
            ("prioridad", "urgente"),
        ]

        for campo, valor in casos:
            with self.subTest(campo=campo, valor=valor):
                with self.assertRaises(ValidationError):
                    self.crear_datos_validos(**{campo: valor})

    def test_contrato_acepta_todos_los_tipos_y_prioridades_acordados(self):
        """Cada valor publicado en el contrato es aceptado por Pydantic."""

        for tipo in TipoNecesidad:
            with self.subTest(tipo=tipo.value):
                necesidad = self.crear_datos_validos(tipo=tipo.value)
                self.assertEqual(necesidad.tipo, tipo)

        for prioridad in ("baja", "media", "alta", "critica"):
            with self.subTest(prioridad=prioridad):
                necesidad = self.crear_datos_validos(prioridad=prioridad)
                self.assertEqual(necesidad.prioridad.value, prioridad)

    def test_rechazar_campos_desconocidos_y_estados_invalidos(self):
        """No se admiten claves adicionales ni estados no publicados."""

        with self.assertRaises(ValidationError):
            self.crear_datos_validos(contacto="dato innecesario")

        with self.assertRaises(ValidationError):
            NecesidadActualizarEstado(estado="cancelada")

    def test_modelos_usan_consultas_parametrizadas(self):
        """El contenido con SQL se almacena literalmente y no altera la tabla."""

        descripcion = "Agua'); DROP TABLE necesidades; --"
        creada = crear_necesidad(
            self.crear_datos_validos(descripcion=descripcion)
        )

        self.assertEqual(creada["descripcion"], descripcion)
        with database.get_cursor() as cursor:
            total = cursor.execute(
                "SELECT COUNT(*) FROM necesidades"
            ).fetchone()[0]
        self.assertEqual(total, 1)


if __name__ == "__main__":
    unittest.main()
