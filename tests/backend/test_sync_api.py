import sqlite3
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from sync.sync_controller import router, get_db

app = FastAPI()
app.include_router(router)
client = TestClient(app)

# FIX: Create a single persistent in-memory database connection for the entire test run.
# check_same_thread=False allows FastAPI's TestClient to safely use it across async threads.
shared_test_conn = sqlite3.connect(":memory:", check_same_thread=False)
cursor = shared_test_conn.cursor()
cursor.execute("""
    CREATE TABLE sync_operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation_id TEXT NOT NULL UNIQUE,
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        operation_type TEXT NOT NULL CHECK (operation_type IN ('CREATE', 'UPDATE', 'DELETE')),
        status TEXT NOT NULL CHECK (status IN ('PENDING', 'APPLIED', 'ALREADY_APPLIED', 'CONFLICT', 'INVALID', 'RETRYABLE_ERROR')),
        payload TEXT NOT NULL,
        client_created_at TEXT NOT NULL
    )
""")
shared_test_conn.commit()

def override_get_db():
    # Yield the shared connection; do NOT close it between requests
    yield shared_test_conn

app.dependency_overrides[get_db] = override_get_db

def test_sync_batch_endpoint_success():
    """Verify the API accepts a valid batch and returns 200 OK with APPLIED status."""
    payload = {
        "operations": [
            {
                "operation_id": "op-api-001",
                "entity_type": "PERSONA",
                "entity_id": "p-100",
                "operation_type": "CREATE",
                "payload": {"estado": "desaparecido"},
                "client_created_at": "2026-08-24T12:00:00Z"
            }
        ]
    }
    
    response = client.post("/api/sync/batch", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["operation_id"] == "op-api-001"
    assert data["results"][0]["status"] == "APPLIED"

def test_sync_batch_endpoint_idempotency():
    """Verify the API handles duplicate network requests safely."""
    payload = {
        "operations": [
            {
                "operation_id": "op-api-002",
                "entity_type": "PERSONA",
                "entity_id": "p-101",
                "operation_type": "CREATE",
                "payload": {"estado": "estoy_bien"},
                "client_created_at": "2026-08-24T12:00:00Z"
            }
        ]
    }
    
    # First request simulates the initial offline sync
    res1 = client.post("/api/sync/batch", json=payload)
    assert res1.json()["results"][0]["status"] == "APPLIED"
    
    # Second request simulates a retry due to poor connectivity
    res2 = client.post("/api/sync/batch", json=payload)
    assert res2.json()["results"][0]["status"] == "ALREADY_APPLIED"