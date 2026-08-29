"""Tests de los endpoints del módulo de necesidades.

Estas pruebas comprueban la capa HTTP definida en routes.py.
Las funciones de acceso a la base de datos se sustituyen temporalmente
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
    "latitud": 39.4699,
    "longitud": -0.3763,
    "prioridad": "alta",
    "id": 1,
    "estado": "abierta",
    "creado_en": "2026-08-21T14:00:00Z",
}


@pytest.fixture
def client():
    """Crea un cliente HTTP aislado para probar únicamente este router."""

    # Creamos una aplicación pequeña exclusiva para estas pruebas.
    test_app = FastAPI()

    # Añadimos las mismas rutas de necesidades que utiliza la aplicación real.
    test_app.include_router(routes.router)

    # TestClient permite realizar peticiones HTTP sin iniciar Uvicorn.
    return TestClient(test_app)


def test_get_needs_returns_list(client, monkeypatch):
    """GET /api/necesidades devuelve las necesidades con código 200."""

    # Esta función sustituye temporalmente a list_needs de models.py.
    # En vez de consultar SQLite, devuelve nuestro dato ficticio.
    def fake_list_needs(status=None, need_type=None):
        return [SAMPLE_NEED]

    # Sustituimos durante este test la función que consulta las necesidades.
    monkeypatch.setattr(routes, "list_needs", fake_list_needs)

    # Simulamos la misma petición GET que ejecutamos desde Swagger.
    response = client.get("/api/necesidades")

    # Comprobamos que la petición ha sido correcta.
    assert response.status_code == 200

    # Convertimos la respuesta JSON a una lista de Python.
    response_body = response.json()

    # Comprobamos que se ha devuelto exactamente una necesidad.
    assert len(response_body) == 1

    # Comprobamos algunos campos importantes del contrato público.
    assert response_body[0]["id"] == 1
    assert response_body[0]["titulo"] == "Agua potable"
    assert response_body[0]["tipo"] == "agua"
    assert response_body[0]["estado"] == "abierta"

    # Verificamos que el JSON público conserva los nombres en español.
    assert "creado_en" in response_body[0]
    assert "created_at" not in response_body[0]


def test_get_needs_passes_type_and_status_filters(client, monkeypatch):
    """GET transmite correctamente los filtros tipo y estado."""

    # Aquí guardaremos los filtros recibidos por la función falsa.
    received_filters = {}

    def fake_list_needs(status=None, need_type=None):
        # Guardamos los filtros para comprobarlos posteriormente.
        received_filters["status"] = status
        received_filters["need_type"] = need_type
        return [SAMPLE_NEED]

    monkeypatch.setattr(routes, "list_needs", fake_list_needs)

    # Enviamos los filtros como parámetros de consulta de la URL.
    response = client.get("/api/necesidades?tipo=agua&estado=abierta")

    assert response.status_code == 200

    # La ruta convierte los textos recibidos en los enums correspondientes.
    assert received_filters["need_type"].value == "agua"
    assert received_filters["status"].value == "abierta"

    # La respuesta mantiene el contrato público en español.
    response_body = response.json()
    assert response_body[0]["tipo"] == "agua"
    assert response_body[0]["estado"] == "abierta"


def test_create_need_returns_201(client, monkeypatch):
    """POST /api/necesidades crea una necesidad y devuelve código 201."""

    received_data = {}

    def fake_create_need(need):
        # Convertimos el esquema recibido en un diccionario que utiliza
        # los alias públicos en español.
        received_data["need"] = need.model_dump(by_alias=True)

        # Simulamos el resultado devuelto después de guardar la necesidad.
        return SAMPLE_NEED

    monkeypatch.setattr(routes, "create_need", fake_create_need)

    # Datos que enviaría el formulario del frontend.
    request_body = {
        "titulo": "Agua potable",
        "tipo": "agua",
        "descripcion": "Punto sin agua potable desde hace dos días",
        "latitud": 39.4699,
        "longitud": -0.3763,
        "prioridad": "alta",
    }

    response = client.post(
        "/api/necesidades",
        json=request_body,
    )

    # 201 significa que el recurso se ha creado correctamente.
    assert response.status_code == 201

    # Comprobamos que la ruta recibió los datos enviados.
    assert received_data["need"]["titulo"] == "Agua potable"
    assert received_data["need"]["tipo"] == "agua"
    assert received_data["need"]["prioridad"] == "alta"

    # Comprobamos la respuesta pública enviada al frontend.
    response_body = response.json()
    assert response_body["id"] == 1
    assert response_body["estado"] == "abierta"
    assert response_body["titulo"] == "Agua potable"
    assert "creado_en" in response_body


def test_update_need_status_returns_200(client, monkeypatch):
    """PATCH actualiza el estado y devuelve código 200."""

    received_data = {}

    def fake_update_need_status(need_id, status):
        # Guardamos los argumentos recibidos para comprobar que la ruta
        # transmite correctamente el identificador y el nuevo estado.
        received_data["need_id"] = need_id
        received_data["status"] = status

        # Simulamos una necesidad que ha quedado cubierta.
        return {
            **SAMPLE_NEED,
            "estado": "cubierta",
        }

    monkeypatch.setattr(
        routes,
        "update_need_status",
        fake_update_need_status,
    )

    response = client.patch(
        "/api/necesidades/1/estado",
        json={"estado": "cubierta"},
    )

    assert response.status_code == 200

    # Comprobamos qué valores recibió la función del modelo.
    assert received_data["need_id"] == 1
    assert received_data["status"].value == "cubierta"

    # Comprobamos el JSON devuelto al frontend.
    response_body = response.json()
    assert response_body["id"] == 1
    assert response_body["estado"] == "cubierta"


def test_update_missing_need_returns_404(client, monkeypatch):
    """PATCH devuelve 404 cuando el identificador no existe."""

    def fake_update_need_status(need_id, status):
        # models.py devuelve None cuando no encuentra la necesidad.
        return None

    monkeypatch.setattr(
        routes,
        "update_need_status",
        fake_update_need_status,
    )

    response = client.patch(
        "/api/necesidades/99999/estado",
        json={"estado": "cubierta"},
    )

    assert response.status_code == 404

    # Comprobamos el formato de error acordado en las convenciones.
    response_body = response.json()
    assert response_body == {
        "error": "Necesidad no encontrada",
        "detalle": ("No existe una necesidad con el identificador 99999."),
    }

    # Verificamos que no aparece el formato automático de HTTPException.
    assert "detail" not in response_body


def test_invalid_status_transition_returns_409(client, monkeypatch):
    """PATCH devuelve 409 cuando la transición no está permitida."""

    def fake_update_need_status(need_id, status):
        # Simulamos la excepción que models.py produce al detectar
        # una transición de estado no permitida.
        raise routes.InvalidStatusTransition

    monkeypatch.setattr(
        routes,
        "update_need_status",
        fake_update_need_status,
    )

    # Intentamos cambiar directamente de abierta a cubierta.
    response = client.patch(
        "/api/necesidades/1/estado",
        json={"estado": "cubierta"},
    )

    assert response.status_code == 409

    # Comprobamos el formato común definido en las convenciones.
    response_body = response.json()
    assert response_body == {
        "error": "Transición de estado no válida",
        "detalle": (
            "La necesidad no puede saltar estados, " "retroceder ni reabrirse."
        ),
    }

    assert "detail" not in response_body


def test_invalid_status_returns_422_before_calling_model(
    client,
    monkeypatch,
):
    """Un estado desconocido se rechaza antes de ejecutar el modelo."""

    model_was_called = {"value": False}

    def fake_update_need_status(need_id, status):
        # Si esta función llegara a ejecutarse, el test lo detectaría.
        model_was_called["value"] = True
        return SAMPLE_NEED

    monkeypatch.setattr(
        routes,
        "update_need_status",
        fake_update_need_status,
    )

    response = client.patch(
        "/api/necesidades/1/estado",
        json={"estado": "inventado"},
    )

    # FastAPI y Pydantic rechazan el estado porque no pertenece al enum.
    assert response.status_code == 422

    # La petición se detiene durante la validación, antes de entrar
    # en la lógica que modifica la base de datos.
    assert model_was_called["value"] is False
