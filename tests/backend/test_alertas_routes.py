"""Tests de los endpoints del módulo de alertas del gestor (Grupo 2, parte Juan).

Comprueba la capa HTTP de routes.py. Las funciones de models.py se sustituyen
temporalmente con monkeypatch para que los tests sean rápidos, aislados y
repetibles, igual que en test_necesidades_routes.py.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from modules.alertas import routes

ZONA = {
    "type": "Polygon",
    "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
}


def fake_row(**over):
    """Construye una fila SQLite simulada de la tabla alertas del gestor."""
    base = {
        "id": 1,
        "nivel_riesgo": "medio",
        "zona": ZONA,
        "activa": 0,
        "gestor_token": "token-juan",
        "titulo": "Zona afectada",
        "descripcion": "Descripcion de prueba",
        "tipo": None,
        "fuente": "gestor",
        "latitud": None,
        "longitud": None,
    }
    base.update(over)
    return base


@pytest.fixture
def client():
    """Crea un cliente HTTP aislado para probar únicamente este router."""
    test_app = FastAPI()
    test_app.include_router(routes.router)
    return TestClient(test_app)


# ---------------------------------------------------------------------------
# Creación
# ---------------------------------------------------------------------------

def test_crear_alerta_devuelve_201(client, monkeypatch):
    """POST /api/alertas crea la alerta y expone el contrato del mapa."""
    captured = {}

    def fake_create(payload):
        captured["payload"] = payload
        return fake_row()

    monkeypatch.setattr(routes, "create_alert", fake_create)

    body = {
        "nivel_riesgo": "medio",
        "zona": ZONA,
        "gestor_token": "token-juan",
        "titulo": "Zona afectada",
        "descripcion": "Descripcion de prueba",
    }
    response = client.post("/api/alertas", json=body)

    assert response.status_code == 201
    data = response.json()
    # Contrato del mapa (Equipo 4)
    assert data["id"] == "1"
    assert data["risk_level"] == "medio"
    assert data["status"] == "inactive"
    assert data["zone"] == ZONA
    # El token solo se expone en creación/consulta individual
    assert data["gestor_token"] == "token-juan"
    assert data["nivel_riesgo"] == "medio"


def test_crear_alerta_nivel_invalido_devuelve_422(client, monkeypatch):
    """Un nivel de riesgo fuera del enum se rechaza antes de tocar el modelo."""
    called = {"value": False}

    def fake_create(payload):
        called["value"] = True
        return fake_row()

    monkeypatch.setattr(routes, "create_alert", fake_create)

    body = {"nivel_riesgo": "critico", "zona": ZONA, "gestor_token": "x"}
    response = client.post("/api/alertas", json=body)

    assert response.status_code == 422
    assert called["value"] is False


def test_crear_alerta_sin_token_devuelve_422(client, monkeypatch):
    """El gestor_token es obligatorio."""
    called = {"value": False}
    monkeypatch.setattr(routes, "create_alert", lambda p: called.update(value=True) or fake_row())

    response = client.post("/api/alertas", json={"nivel_riesgo": "bajo", "zona": ZONA})

    assert response.status_code == 422
    assert called["value"] is False


# ---------------------------------------------------------------------------
# Lectura
# ---------------------------------------------------------------------------

def test_listar_alertas_devuelve_200(client, monkeypatch):
    """GET /api/alertas combina externas y del gestor."""
    monkeypatch.setattr(
        routes.services,
        "combined_alerts",
        lambda tipo=None, severidad=None, pais=None: [fake_row()],
    )
    response = client.get("/api/alertas")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert str(body[0]["id"]) == "1"


def test_obtener_alerta_devuelve_200(client, monkeypatch):
    """GET /api/alertas/{id} devuelve la alerta con su token."""
    monkeypatch.setattr(routes, "get_alert", lambda aid: fake_row())
    response = client.get("/api/alertas/1")
    assert response.status_code == 200
    assert response.json()["gestor_token"] == "token-juan"


def test_obtener_alerta_inexistente_devuelve_404(client, monkeypatch):
    """GET /api/alertas/{id} con id inexistente -> 404."""
    monkeypatch.setattr(routes, "get_alert", lambda aid: None)
    response = client.get("/api/alertas/99999")
    assert response.status_code == 404
    assert "detail" in response.json()


# ---------------------------------------------------------------------------
# Activación / nivel de riesgo
# ---------------------------------------------------------------------------

def test_activar_alerta_devuelve_200(client, monkeypatch):
    """POST /api/alertas/{id}/activar -> estado active."""
    monkeypatch.setattr(routes, "set_activation", lambda aid, activa, alto_riesgo=False: fake_row(activa=1))
    response = client.post("/api/alertas/1/activar")
    assert response.status_code == 200
    assert response.json()["status"] == "active"
    assert response.json()["activa"] is True


def test_alto_riesgo_alerta_devuelve_200(client, monkeypatch):
    """POST /api/alertas/{id}/alto-riesgo fija nivel alto y estado alto_riesgo."""
    monkeypatch.setattr(
        routes, "set_activation",
        lambda aid, activa, alto_riesgo=False: fake_row(activa=1, nivel_riesgo="alto"),
    )
    response = client.post("/api/alertas/1/alto-riesgo")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alto_riesgo"
    assert data["risk_level"] == "alto"


def test_desactivar_alerta_devuelve_200(client, monkeypatch):
    """POST /api/alertas/{id}/desactivar -> estado inactive."""
    monkeypatch.setattr(routes, "set_activation", lambda aid, activa, alto_riesgo=False: fake_row(activa=0))
    response = client.post("/api/alertas/1/desactivar")
    assert response.status_code == 200
    assert response.json()["status"] == "inactive"


def test_activar_alerta_inexistente_devuelve_404(client, monkeypatch):
    """Activar un id inexistente -> 404."""
    monkeypatch.setattr(routes, "set_activation", lambda aid, activa, alto_riesgo=False: None)
    response = client.post("/api/alertas/99999/activar")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Actualización
# ---------------------------------------------------------------------------

def test_actualizar_alerta_devuelve_200(client, monkeypatch):
    """PATCH /api/alertas/{id} aplica los cambios."""
    monkeypatch.setattr(routes, "update_alert", lambda aid, payload: fake_row(nivel_riesgo="bajo", titulo="Cambiado"))
    response = client.patch("/api/alertas/1", json={"nivel_riesgo": "bajo", "titulo": "Cambiado"})
    assert response.status_code == 200
    data = response.json()
    assert data["nivel_riesgo"] == "bajo"
    assert data["titulo"] == "Cambiado"


def test_actualizar_alerta_inexistente_devuelve_404(client, monkeypatch):
    """PATCH sobre id inexistente -> 404."""
    monkeypatch.setattr(routes, "update_alert", lambda aid, payload: None)
    response = client.patch("/api/alertas/99999", json={"titulo": "x"})
    assert response.status_code == 404


def test_actualizar_alerta_nivel_invalido_devuelve_422(client, monkeypatch):
    """PATCH con nivel fuera del enum se rechaza con 422."""
    called = {"value": False}
    monkeypatch.setattr(routes, "update_alert", lambda aid, payload: called.update(value=True) or fake_row())
    response = client.patch("/api/alertas/1", json={"nivel_riesgo": "fuego"})
    assert response.status_code == 422
    assert called["value"] is False
