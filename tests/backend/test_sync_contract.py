import sqlite3

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sync.sync_controller import get_db, router


def create_sync_schema(conn):
    conn.execute(
        """
        CREATE TABLE sync_operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation_id TEXT NOT NULL UNIQUE,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            operation_type TEXT NOT NULL CHECK (operation_type IN ('CREATE', 'UPDATE', 'DELETE')),
            status TEXT NOT NULL CHECK (
                status IN (
                    'PENDING',
                    'APPLIED',
                    'ALREADY_APPLIED',
                    'CONFLICT',
                    'INVALID',
                    'RETRYABLE_ERROR'
                )
            ),
            payload TEXT NOT NULL,
            client_created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def make_client():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    create_sync_schema(conn)

    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        yield conn

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app), conn


def make_operation(operation_id="op-contract-001"):
    return {
        "operation_id": operation_id,
        "entity_type": "PERSONA",
        "entity_id": "p-contract-001",
        "operation_type": "CREATE",
        "payload": {"estado": "estoy_bien", "version": 1},
        "client_created_at": "2026-08-24T12:00:00Z",
    }


def test_sync_batch_is_current_backend_contract():
    client, conn = make_client()
    response = client.post(
        "/api/sync/batch",
        json={"operations": [make_operation()]},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {
        "results": [
            {
                "operation_id": "op-contract-001",
                "status": "APPLIED",
            }
        ]
    }

    persisted = conn.execute(
        "SELECT operation_id, status FROM sync_operations WHERE operation_id = ?",
        ("op-contract-001",),
    ).fetchone()
    assert persisted == ("op-contract-001", "APPLIED")


def test_sync_root_endpoint_is_not_implemented_and_must_not_be_used_by_frontend():
    client, _ = make_client()
    response = client.post(
        "/api/sync",
        json={"operations": [make_operation("op-root-contract-001")]},
    )

    assert response.status_code == 404
