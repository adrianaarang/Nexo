import sqlite3
import pytest
from sync.services import process_sync_batch

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
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
    conn.commit()
    yield conn
    conn.close()

def test_sync_conflict_stale_update(db_conn):
    """MANDATORY TEST: Verify that updating with an older version returns CONFLICT."""
    
    operations = [
        {
            "operation_id": "op-conflict-01",
            "entity_type": "PERSONA",
            "entity_id": "p-200", # We mocked this entity to be at version 3 on the server
            "operation_type": "UPDATE",
            "payload": {"estado": "localizado", "version": 2}, # Client only knows about version 2
            "client_created_at": "2026-08-24T13:00:00Z"
        },
        {
            "operation_id": "op-valid-update",
            "entity_type": "PERSONA",
            "entity_id": "p-200",
            "operation_type": "UPDATE",
            "payload": {"estado": "seguro", "version": 3}, # Client is up to date
            "client_created_at": "2026-08-24T13:05:00Z"
        }
    ]
    
    results = process_sync_batch(db_conn, operations)
    
    # The stale update should be rejected
    assert results[0]["operation_id"] == "op-conflict-01"
    assert results[0]["status"] == "CONFLICT"
    
    # The up-to-date update should be applied
    assert results[1]["operation_id"] == "op-valid-update"
    assert results[1]["status"] == "APPLIED"