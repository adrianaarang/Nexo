"""Pruebas pytest de persistencia y validación del módulo de personas."""
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pydantic import ValidationError

from db import database
from modules.personas.models import mark_person_safe
from modules.personas.schemas import (
    PersonResponse,
    PersonSafeRequest,
    PersonStatus,
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


def create_person(
    *,
    name="Josep Martí",
    status="desaparecida",
    last_location="Paiporta, cerca del puente",
    reported_by="familia",
):
    """Inserta una persona de prueba y devuelve su registro completo."""

    with database.get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO personas
               (nombre, estado, ultima_ubicacion, reportado_por)
               VALUES (?, ?, ?, ?)""",
            (
                name,
                status,
                last_location,
                reported_by,
            ),
        )
        person_id = cursor.lastrowid

        cursor.execute(
            "SELECT * FROM personas WHERE id = ?",
            (person_id,),
        )
        return dict(cursor.fetchone())


def test_mark_person_safe_updates_existing_person():
    """Una persona registrada puede comunicar que se encuentra bien."""

    created = create_person()

    updated = mark_person_safe(created["id"])

    assert updated is not None
    assert updated["id"] == created["id"]
    assert updated["estado"] == "estoy_bien"

    # La operación de estado no debe modificar los demás datos existentes.
    assert updated["nombre"] == created["nombre"]
    assert updated["ultima_ubicacion"] == created["ultima_ubicacion"]
    assert updated["reportado_por"] == created["reportado_por"]
    assert updated["creado_en"] == created["creado_en"]


def test_mark_person_safe_returns_persisted_record():
    """El resultado coincide con el estado realmente guardado en SQLite."""

    created = create_person()

    updated = mark_person_safe(created["id"])

    with database.get_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM personas WHERE id = ?",
            (created["id"],),
        )
        persisted = dict(cursor.fetchone())

    assert updated == persisted
    assert persisted["estado"] == PersonStatus.SAFE.value


def test_mark_person_safe_is_idempotent():
    """Repetir la declaración Estoy Bien devuelve el mismo registro."""

    created = create_person()

    first_result = mark_person_safe(created["id"])
    second_result = mark_person_safe(created["id"])

    assert first_result == second_result
    assert second_result["estado"] == "estoy_bien"


def test_mark_missing_person_returns_none():
    """Un identificador inexistente puede traducirse después a HTTP 404."""

    assert mark_person_safe(999) is None


def test_person_response_matches_public_json_contract():
    """La respuesta pública conserva los nombres de campos en español."""

    created = create_person()
    updated = mark_person_safe(created["id"])

    response = PersonResponse.model_validate(updated).model_dump(
        mode="json",
        by_alias=True,
    )

    assert response["id"] == created["id"]
    assert response["nombre"] == "Josep Martí"
    assert response["estado"] == "estoy_bien"
    assert response["ultima_ubicacion"] == "Paiporta, cerca del puente"
    assert response["reportado_por"] == "familia"
    assert "creado_en" in response

    assert "name" not in response
    assert "status" not in response
    assert "created_at" not in response


def test_safe_request_accepts_public_person_id():
    """El contrato público acepta un identificador positivo."""

    request = PersonSafeRequest.model_validate(
        {
            "id_persona": 1,
        }
    )

    assert request.person_id == 1


@pytest.mark.parametrize(
    "payload",
    [
        {"id_persona": 0},
        {"id_persona": -1},
        {"id_persona": 1, "campo_inventado": "dato"},
        {"person_id": 1},
    ],
)
def test_safe_request_rejects_invalid_payloads(payload):
    """Rechaza ids inválidos, campos extra y nombres internos de Python."""

    with pytest.raises(ValidationError):
        PersonSafeRequest.model_validate(payload)
