"""Pruebas pytest de las capas de persistencia, servicios y validación
del módulo de necesidades (rediseño: 8 categorías, estados abierta/cubierta,
título por defecto en services.py)."""
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pydantic import ValidationError

from db import database
from modules.necesidades import services
from modules.necesidades.models import InvalidStatusTransition, get_need
from modules.necesidades.schemas import (
    NeedCreate,
    NeedResponse,
    NeedStatus,
    NeedStatusUpdate,
    NeedType,
)


@pytest.fixture(autouse=True)
def temporary_database():
    """Crea una base de datos SQLite aislada para cada prueba."""

    previous_path = database.DATABASE_PATH
    with TemporaryDirectory() as temp_directory:
        database.DATABASE_PATH = str(Path(temp_directory) / "nexo_test.db")
        database.init_db()
        try:
            yield
        finally:
            database.DATABASE_PATH = previous_path


def build_valid_need(**changes) -> NeedCreate:
    """Construye datos válidos y permite variar un campo en cada prueba."""

    payload = {
        "titulo": "Agua potable y mantas",
        "tipo": "agua",
        "descripcion": "Se necesita agua potable",
        "direccion": "Calle Mayor 3, Valencia",
        "latitud": 39.4699,
        "longitud": -0.3763,
    }
    payload.update(changes)
    return NeedCreate(**payload)


def test_create_and_get_need_with_normalized_values():
    """La creación devuelve una fila completa recuperable por su id."""

    need = build_valid_need(descripcion="  Agua para el refugio  ")

    created = services.create_need(need)

    assert created == services.get_need(created["id"])
    assert created["titulo"] == "Agua potable y mantas"
    assert created["descripcion"] == "Agua para el refugio"
    assert created["prioridad"] == "media"
    assert created["estado"] == "abierta"
    assert NeedResponse.model_validate(created).id == created["id"]


def test_create_need_without_title_uses_category_default():
    """El formulario simplificado puede omitir el título; el servicio lo genera."""

    created = services.create_need(build_valid_need(titulo="", tipo="parafarmacia"))

    assert created["titulo"] == "Necesidad de parafarmacia"


def test_create_need_without_description_is_allowed():
    """La descripción también es opcional en el formulario simplificado."""

    created = services.create_need(build_valid_need(descripcion=""))

    assert created["descripcion"] == ""


def test_create_need_stores_the_geocoded_address():
    """La dirección legible (geocodificada en el frontend) se guarda tal cual."""

    created = services.create_need(
        build_valid_need(direccion="Plaza del Ayuntamiento, Valencia")
    )

    assert created["direccion"] == "Plaza del Ayuntamiento, Valencia"


def test_create_need_without_address_is_allowed():
    """La dirección es opcional: puede llegar vacía si solo hay coordenadas."""

    created = services.create_need(build_valid_need(direccion=""))

    assert created["direccion"] == ""


def test_create_need_truncates_very_long_nominatim_addresses():
    """Nominatim puede devolver direcciones larguísimas; no deben rechazarse."""

    # Ejemplo realista de lo que devuelve Nominatim en display_name: calle,
    # barrio, distrito, ciudad, comarca, provincia, código postal, país...
    direccion_base = (
        "60, Carrer de Sant Vicent Màrtir, El Pilar, Extramurs, València, "
        "Comarca de València, València / Valencia, Comunitat Valenciana, "
        "46007, España"
    )
    direccion_larga = direccion_base * 3
    assert len(direccion_larga) > 300

    created = services.create_need(build_valid_need(direccion=direccion_larga))

    assert created["direccion"] == direccion_larga[:300]


def test_migration_converts_values_from_the_previous_contract():
    """Una base existente conserva sus filas al adoptar el contrato nuevo."""

    with database.get_cursor() as cursor:
        cursor.execute("DROP TABLE necesidades")
        cursor.execute("DELETE FROM schema_migrations")
        cursor.execute(
            """CREATE TABLE necesidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK (
                    tipo IN ('agua', 'alimento', 'medicina', 'refugio',
                             'herramientas', 'transporte')
                ),
                descripcion TEXT NOT NULL,
                latitud REAL NOT NULL,
                longitud REAL NOT NULL,
                prioridad TEXT NOT NULL DEFAULT 'media',
                estado TEXT NOT NULL DEFAULT 'abierta' CHECK (
                    estado IN ('abierta', 'en_proceso', 'cubierta')
                ),
                creado_en TEXT NOT NULL
            )"""
        )
        cursor.execute(
            """INSERT INTO necesidades
               (titulo, tipo, descripcion, latitud, longitud, prioridad,
                estado, creado_en)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                "Insulina",
                "medicina",
                "Tratamiento urgente",
                39.4,
                -0.3,
                "critica",
                "en_proceso",
                "2026-08-21T14:00:00Z",
            ),
        )

    database.init_db()
    migrated = services.list_needs()

    assert migrated[0]["tipo"] == "parafarmacia"
    assert migrated[0]["estado"] == "abierta"
    assert migrated[0]["direccion"] == ""


def test_stored_record_matches_the_shared_json_contract():
    """El contrato acordado conserva los nombres externos en español."""

    created = services.create_need(
        NeedCreate(
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

    response = NeedResponse.model_validate(created).model_dump(
        mode="json",
        by_alias=True,
    )

    assert isinstance(response["id"], int)
    assert response["titulo"] == "Agua potable y mantas"
    assert response["tipo"] == "agua"
    assert response["prioridad"] == "alta"
    assert response["estado"] == "abierta"
    assert response["creado_en"].endswith("Z")
    # Etiqueta con emoji lista para pintar en el mapa/tarjeta.
    assert response["categoria_etiqueta"] == "💧 Agua"


def test_list_needs_filters_by_status_and_type():
    """Los filtros opcionales devuelven únicamente los registros coincidentes."""

    water = services.create_need(build_valid_need())
    services.create_need(
        build_valid_need(
            titulo="Comida caliente",
            tipo="alimentos",
            descripcion="Comida caliente",
        )
    )
    services.update_need_status(water["id"], NeedStatus.COVERED)

    covered = services.list_needs(status=NeedStatus.COVERED)
    food = services.list_needs(need_type=NeedType.FOOD)

    assert [row["id"] for row in covered] == [water["id"]]
    assert [row["tipo"] for row in food] == ["alimentos"]


def test_update_need_status_returns_the_persisted_record():
    """La única transición válida (abierta -> cubierta) devuelve la fila actualizada."""

    created = services.create_need(build_valid_need())

    updated = services.update_need_status(created["id"], NeedStatus.COVERED)

    assert updated["estado"] == "cubierta"


def test_missing_ids_return_none():
    """Las rutas pueden traducir los registros inexistentes a respuestas HTTP 404."""

    assert get_need(999) is None
    assert services.update_need_status(999, NeedStatus.COVERED) is None


def test_status_only_advances_from_open_to_covered():
    """Repetir el estado actual es idempotente; no se puede reabrir una cubierta."""

    created = services.create_need(build_valid_need())

    covered = services.update_need_status(created["id"], NeedStatus.COVERED)
    repeated = services.update_need_status(created["id"], NeedStatus.COVERED)
    assert covered == repeated

    with pytest.raises(InvalidStatusTransition):
        services.update_need_status(created["id"], NeedStatus.OPEN)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("tipo", "medicina"),
        ("tipo", "herramientas"),
        ("titulo", "x" * 121),
        ("latitud", 90.1),
        ("longitud", -180.1),
        ("latitud", float("nan")),
        ("prioridad", "urgente"),
    ],
)
def test_creation_rejects_invalid_fields(field, value):
    """Los enums, límites de texto y rangos geográficos protegen el contrato."""

    with pytest.raises(ValidationError):
        build_valid_need(**{field: value})


@pytest.mark.parametrize("need_type", list(NeedType))
def test_contract_accepts_every_agreed_need_type(need_type):
    """Acepta las 8 categorías cerradas publicadas en el contrato."""

    assert build_valid_need(tipo=need_type.value).need_type == need_type


@pytest.mark.parametrize("priority", ["baja", "media", "alta", "critica"])
def test_contract_accepts_every_agreed_priority(priority):
    """Acepta todas las prioridades publicadas en el contrato."""

    assert build_valid_need(prioridad=priority).priority.value == priority


def test_unknown_fields_and_statuses_are_rejected():
    """Rechaza las claves inesperadas y los estados no publicados."""

    with pytest.raises(ValidationError):
        build_valid_need(contacto="dato innecesario")

    # Los nombres internos en inglés no forman parte del contrato JSON público.
    with pytest.raises(ValidationError):
        build_valid_need(title="Nombre fuera del contrato")

    with pytest.raises(ValidationError):
        NeedStatusUpdate(estado="en_proceso")

    with pytest.raises(ValidationError):
        NeedStatusUpdate(estado="cancelada")

    with pytest.raises(ValidationError):
        NeedStatusUpdate(status="covered")


def test_models_use_parameterized_queries():
    """El contenido similar a SQL se guarda literalmente sin alterar la tabla."""

    description = "Agua'); DROP TABLE necesidades; --"
    created = services.create_need(build_valid_need(descripcion=description))

    assert created["descripcion"] == description
    with database.get_cursor() as cursor:
        total = cursor.execute("SELECT COUNT(*) FROM necesidades").fetchone()[0]
    assert total == 1
