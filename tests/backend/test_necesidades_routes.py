"""Tests de los endpoints del módulo de necesidades.

Estas pruebas comprueban la capa HTTP definida en routes.py.
Las funciones de la capa de servicios se sustituyen temporalmente
para que los tests sean rápidos, independientes y repetibles.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from modules.necesidades import routes

# Este diccionario representa una necesidad válida devuelta por el backend.
# Se reutiliza en diferentes tests para evitar repetir los mismos datos.
SAMPLE_NEED = {
    "titulo": "Agua potable",
    "tipo": "agua",
    "descripcion": "Punto sin agua potable desde hace dos días",
    "direccion": "Calle Mayor 3, Valencia",
    "latitud": 39.4699,
    "longitud": -0.3763,
    "prioridad": "alta",
    "id": 1,
    "estado": "abierta",
    "creado_en": "2026-08-21T14:00:00Z",
    "categoria_etiqueta": "💧 Agua",
}


@pytest.fixture
def client():
    """Crea un cliente HTTP aislado para probar únicamente este router."""

    test_app = FastAPI()
    test_app.include_router(routes.router)

    return TestClient(test_app)


def test_get_needs_returns_list(client, monkeypatch):
    """GET /api/necesidades devuelve las necesidades con código 200."""

    def fake_list_needs(status=None, need_type=None):
        return [SAMPLE_NEED]

    monkeypatch.setattr(routes, "list_needs", fake_list_needs)

    response = client.get("/api/necesidades")

    assert response.status_code == 200

    response_body = response.json()

    assert len(response_body) == 1
    assert response_body[0]["id"] == 1
    assert response_body[0]["titulo"] == "Agua potable"
    assert response_body[0]["tipo"] == "agua"
    assert response_body[0]["estado"] == "abierta"
    assert response_body[0]["categoria_etiqueta"] == "💧 Agua"

    # Verificamos que el JSON público conserva los nombres en español.
    assert "creado_en" in response_body[0]
    assert "created_at" not in response_body[0]


def test_get_needs_passes_type_and_status_filters(client, monkeypatch):
    """GET transmite correctamente los filtros tipo y estado."""

    received_filters = {}

    def fake_list_needs(status=None, need_type=None):
        received_filters["status"] = status
        received_filters["need_type"] = need_type
        return [SAMPLE_NEED]

    monkeypatch.setattr(routes, "list_needs", fake_list_needs)

    response = client.get("/api/necesidades?tipo=agua&estado=abierta")

    assert response.status_code == 200
    assert received_filters["need_type"].value == "agua"
    assert received_filters["status"].value == "abierta"

    response_body = response.json()
    assert response_body[0]["tipo"] == "agua"
    assert response_body[0]["estado"] == "abierta"


def test_get_need_by_id_returns_200(client, monkeypatch):
    """GET /api/necesidades/{id} devuelve una única necesidad."""

    def fake_get_need(need_id):
        assert need_id == 1
        return SAMPLE_NEED

    monkeypatch.setattr(routes, "get_need", fake_get_need)

    response = client.get("/api/necesidades/1")

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == 1
    assert response_body["titulo"] == "Agua potable"


def test_get_need_by_id_returns_404_when_missing(client, monkeypatch):
    """GET /api/necesidades/{id} devuelve 404 con el formato único de error."""

    monkeypatch.setattr(routes, "get_need", lambda need_id: None)

    response = client.get("/api/necesidades/99999")

    assert response.status_code == 404
    assert response.json() == {
        "error": "Necesidad no encontrada",
        "detalle": "No existe una necesidad con el identificador 99999.",
    }


def test_create_need_returns_201(client, monkeypatch):
    """POST /api/necesidades crea una necesidad y devuelve código 201."""

    received_data = {}

    def fake_create_need(need):
        received_data["need"] = need.model_dump(by_alias=True)
        return SAMPLE_NEED

    monkeypatch.setattr(routes, "create_need", fake_create_need)

    # Datos mínimos que enviaría el formulario simplificado: solo
    # categoría y ubicación son obligatorios.
    request_body = {
        "tipo": "agua",
        "latitud": 39.4699,
        "longitud": -0.3763,
    }

    response = client.post(
        "/api/necesidades",
        json=request_body,
    )

    assert response.status_code == 201
    assert received_data["need"]["tipo"] == "agua"
    assert received_data["need"]["titulo"] == ""
    assert received_data["need"]["direccion"] == ""

    response_body = response.json()
    assert response_body["id"] == 1
    assert response_body["estado"] == "abierta"
    assert response_body["categoria_etiqueta"] == "💧 Agua"
    assert "creado_en" in response_body


def test_create_need_accepts_geocoded_address(client, monkeypatch):
    """POST acepta la dirección legible que el frontend obtiene al geocodificar."""

    received_data = {}

    def fake_create_need(need):
        received_data["need"] = need.model_dump(by_alias=True)
        return SAMPLE_NEED

    monkeypatch.setattr(routes, "create_need", fake_create_need)

    response = client.post(
        "/api/necesidades",
        json={
            "tipo": "agua",
            "direccion": "Calle Mayor 3, Valencia",
            "latitud": 39.4699,
            "longitud": -0.3763,
        },
    )

    assert response.status_code == 201
    assert received_data["need"]["direccion"] == "Calle Mayor 3, Valencia"


def test_update_need_status_returns_200(client, monkeypatch):
    """PATCH /api/necesidades/{id} actualiza el estado y devuelve código 200."""

    received_data = {}

    def fake_update_need_status(need_id, status):
        received_data["need_id"] = need_id
        received_data["status"] = status
        return {**SAMPLE_NEED, "estado": "cubierta"}

    monkeypatch.setattr(
        routes,
        "update_need_status",
        fake_update_need_status,
    )

    response = client.patch(
        "/api/necesidades/1",
        json={"estado": "cubierta"},
    )

    assert response.status_code == 200
    assert received_data["need_id"] == 1
    assert received_data["status"].value == "cubierta"

    response_body = response.json()
    assert response_body["id"] == 1
    assert response_body["estado"] == "cubierta"


def test_update_missing_need_returns_404(client, monkeypatch):
    """PATCH devuelve 404 cuando el identificador no existe."""

    monkeypatch.setattr(
        routes,
        "update_need_status",
        lambda need_id, status: None,
    )

    response = client.patch(
        "/api/necesidades/99999",
        json={"estado": "cubierta"},
    )

    assert response.status_code == 404
    response_body = response.json()
    assert response_body == {
        "error": "Necesidad no encontrada",
        "detalle": ("No existe una necesidad con el identificador 99999."),
    }
    assert "detail" not in response_body


def test_invalid_status_transition_returns_409(client, monkeypatch):
    """PATCH devuelve 409 cuando se intenta reabrir una necesidad cubierta."""

    def fake_update_need_status(need_id, status):
        raise routes.InvalidStatusTransition

    monkeypatch.setattr(
        routes,
        "update_need_status",
        fake_update_need_status,
    )

    response = client.patch(
        "/api/necesidades/1",
        json={"estado": "abierta"},
    )

    assert response.status_code == 409
    response_body = response.json()
    assert response_body == {
        "error": "Transición de estado no válida",
        "detalle": (
            "La necesidad no puede saltar estados, " "retroceder ni reabrirse."
        ),
    }
    assert "detail" not in response_body


def test_invalid_status_returns_422_before_calling_service(
    client,
    monkeypatch,
):
    """Rechaza un estado retirado antes de llamar al servicio."""

    service_was_called = {"value": False}

    def fake_update_need_status(need_id, status):
        service_was_called["value"] = True
        return SAMPLE_NEED

    monkeypatch.setattr(
        routes,
        "update_need_status",
        fake_update_need_status,
    )

    response = client.patch(
        "/api/necesidades/1",
        json={"estado": "en_proceso"},
    )

    assert response.status_code == 422
    assert service_was_called["value"] is False
