import sqlite3
import pytest

@pytest.fixture
def db_conn():
    """Sets up an isolated in-memory DB with our Phase 2 schema."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Apply our Phase 2 Migration (002_sync_setup.sql)
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

def test_sync_operations_idempotency_constraint(db_conn):
    """Phase 2: Verify the database rejects duplicate operation_ids."""
    cursor = db_conn.cursor()
    
    # 1. Insert the first offline operation
    cursor.execute("""
        INSERT INTO sync_operations (operation_id, entity_type, entity_id, operation_type, status, payload, client_created_at)
        VALUES ('op-123', 'PERSONA', 'p-1', 'CREATE', 'PENDING', '{}', '2026-08-24T10:00:00Z')
    """)
    db_conn.commit()

    # 2. Attempt a duplicate insertion (Simulating a frontend retry)
    with pytest.raises(sqlite3.IntegrityError) as excinfo:
        cursor.execute("""
            INSERT INTO sync_operations (operation_id, entity_type, entity_id, operation_type, status, payload, client_created_at)
            VALUES ('op-123', 'PERSONA', 'p-1', 'CREATE', 'PENDING', '{}', '2026-08-24T10:00:00Z')
        """)
    
    # 3. Prove the database blocked it
    assert "UNIQUE constraint failed: sync_operations.operation_id" in str(excinfo.value)

def test_sync_operations_invalid_status_enum(db_conn):
    """Phase 2: Verify the database rejects invalid status values."""
    cursor = db_conn.cursor()
    
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO sync_operations (operation_id, entity_type, entity_id, operation_type, status, payload, client_created_at)
            VALUES ('op-124', 'PERSONA', 'p-2', 'CREATE', 'UNKNOWN_STATUS', '{}', '2026-08-24T10:00:00Z')
        """)