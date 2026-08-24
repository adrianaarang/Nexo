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

def test_sync_retryable_vs_permanent_errors(db_conn):
    """Verify the backend properly classifies temporary vs permanent errors."""
    
    operations = [
        {
            # Valid operation
            "operation_id": "op-ok-1",
            "entity_type": "PERSONA",
            "entity_id": "p-1",
            "operation_type": "CREATE",
            "payload": {},
            "client_created_at": "2026-08-24T14:00:00Z"
        },
        {
            # Simulate a locked database (transient)
            "operation_id": "op-retry-1",
            "entity_type": "SIMULATE_LOCK",
            "entity_id": "p-2",
            "operation_type": "CREATE",
            "payload": {},
            "client_created_at": "2026-08-24T14:01:00Z"
        },
        {
            # Simulate a permanent error (missing operation_type will break the SQL constraint)
            "operation_id": "op-invalid-1",
            "entity_type": "PERSONA",
            "entity_id": "p-3",
            "operation_type": "BAD_TYPE", 
            "payload": {},
            "client_created_at": "2026-08-24T14:02:00Z"
        }
    ]
    
    results = process_sync_batch(db_conn, operations)
    
    assert results[0]["status"] == "APPLIED"
    assert results[1]["status"] == "RETRYABLE_ERROR"
    assert results[2]["status"] == "INVALID"