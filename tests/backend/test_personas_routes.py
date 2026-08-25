"""Tests de los endpoints del módulo de personas.

Estas pruebas comprueban la capa HTTP de la funcionalidad "Estoy Bien".
El acceso a la base de datos se sustituye temporalmente para mantener los
tests aislados, rápidos y repetibles.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from modules.personas import routes


SAMPLE_PERSON = {
    "id": 1,
    "nombre": "Josep Martí",
    "estado": "estoy_bien",
    "ultima_ubicacion": "Paiporta, cerca del puente",
    "reportado_por": "familia",
    "creado_en": "2026-08-24T12:00:00",
}


@pytest.fixture
def client():
    """Crea un cliente HTTP aislado para probar únicamente este router."""

    test_app = FastAPI()
    test_app.include_router(routes.router)
    return TestClient(test_app)


def test_mark_person_safe_returns_200(client, monkeypatch):
    """POST /estoy-bien marca una persona existente y devuelve código 200."""

    received_data = {}

    def fake_mark_person_safe(person_id):
        received_data["person_id"] = person_id
        return SAMPLE_PERSON

    monkeypatch.setattr(
        routes,
        "mark_person_safe",
        fake_mark_person_safe,
    )

    response = client.post(
        "/api/personas/estoy-bien",
        json={"id_persona": 1},
    )

    assert response.status_code == 200
    assert received_data["person_id"] == 1

    response_body = response.json()
    assert response_body["id"] == 1
    assert response_body["nombre"] == "Josep Martí"
    assert response_body["estado"] == "estoy_bien"
    assert "creado_en" in response_body
    assert "created_at" not in response_body


def test_mark_missing_person_returns_404(client, monkeypatch):
    """POST /estoy-bien devuelve 404 cuando la persona no existe."""

    def fake_mark_person_safe(person_id):
        return None

    monkeypatch.setattr(
        routes,
        "mark_person_safe",
        fake_mark_person_safe,
    )

    response = client.post(
        "/api/personas/estoy-bien",
        json={"id_persona": 999},
    )

    assert response.status_code == 404

    response_body = response.json()
    assert response_body == {
        "error": "Persona no encontrada",
        "detalle": "No existe una persona con el identificador 999.",
    }

    assert "detail" not in response_body


def test_invalid_person_id_returns_422_before_calling_model(
    client,
    monkeypatch,
):
    """Un identificador no positivo se rechaza antes de ejecutar el modelo."""

    model_was_called = {"value": False}

    def fake_mark_person_safe(person_id):
        model_was_called["value"] = True
        return SAMPLE_PERSON

    monkeypatch.setattr(
        routes,
        "mark_person_safe",
        fake_mark_person_safe,
    )

    response = client.post(
        "/api/personas/estoy-bien",
        json={"id_persona": 0},
    )

    assert response.status_code == 422
    assert model_was_called["value"] is False
