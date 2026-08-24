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

def test_process_sync_batch_partial_failure(db_conn):
    """MANDATORY TEST: One bad operation should not rollback the good ones in the batch."""
    
    # op1 is valid. op2 is invalid (unknown operation_type). op3 is valid.
    operations = [
        {"operation_id": "op-1", "entity_type": "PERSONA", "entity_id": "p-1", "operation_type": "CREATE", "payload": {}, "client_created_at": "2026-08-24T10:00:00Z"},
        {"operation_id": "op-2", "entity_type": "PERSONA", "entity_id": "p-2", "operation_type": "UNKNOWN", "payload": {}, "client_created_at": "2026-08-24T10:00:00Z"},
        {"operation_id": "op-3", "entity_type": "PERSONA", "entity_id": "p-3", "operation_type": "CREATE", "payload": {}, "client_created_at": "2026-08-24T10:00:00Z"}
    ]
    
    results = process_sync_batch(db_conn, operations)
    
    # Assert correct statuses are returned to the client
    assert results[0]["status"] == "APPLIED"
    assert results[1]["status"] == "INVALID"
    assert results[2]["status"] == "APPLIED"
    
    # Verify the database actually persisted the valid ones and skipped the invalid one
    cursor = db_conn.cursor()
    cursor.execute("SELECT operation_id FROM sync_operations")
    persisted_ops = [row[0] for row in cursor.fetchall()]
    assert "op-1" in persisted_ops
    assert "op-3" in persisted_ops
    assert "op-2" not in persisted_ops

def test_process_sync_batch_idempotency_service(db_conn):
    """Verify that submitting the same operation twice yields ALREADY_APPLIED the second time."""
    operations = [
        {"operation_id": "op-dup", "entity_type": "PERSONA", "entity_id": "p-dup", "operation_type": "CREATE", "payload": {}, "client_created_at": "2026-08-24T10:00:00Z"}
    ]
    
    # First pass
    res1 = process_sync_batch(db_conn, operations)
    assert res1[0]["status"] == "APPLIED"
    
    # Second pass (retry)
    res2 = process_sync_batch(db_conn, operations)
    assert res2[0]["status"] == "ALREADY_APPLIED"