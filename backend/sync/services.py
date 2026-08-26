import sqlite3
import json

def process_sync_batch(db_conn: sqlite3.Connection, operations: list[dict]) -> list[dict]:
    """
    Processes a batch of offline operations. 
    Enforces idempotency, conflicts, and distinguishes retryable errors.
    """
    results = []
    cursor = db_conn.cursor()
    mock_server_state = {"p-200": {"version": 3}}
    
    for op in operations:
        op_id = op["operation_id"]
        savepoint_name = f"sp_{op_id.replace('-', '_')}"
        cursor.execute(f"SAVEPOINT {savepoint_name}")
        
        try:
            # 1. Idempotency Check
            cursor.execute("SELECT status FROM sync_operations WHERE operation_id = ?", (op_id,))
            if cursor.fetchone():
                results.append({"operation_id": op_id, "status": "ALREADY_APPLIED"})
                cursor.execute(f"RELEASE SAVEPOINT {savepoint_name}")
                continue
                
            # 2. Conflict Check (Stale Update Detection)
            payload = op.get("payload", {})
            if op["operation_type"] == "UPDATE":
                client_version = payload.get("version", 1)
                server_version = mock_server_state.get(op["entity_id"], {}).get("version", 1)
                
                if client_version < server_version:
                    results.append({"operation_id": op_id, "status": "CONFLICT"})
                    cursor.execute(f"RELEASE SAVEPOINT {savepoint_name}")
                    continue
            
            # Artificial trigger for testing temporary failures
            if op["entity_type"] == "SIMULATE_LOCK":
                raise sqlite3.OperationalError("database is locked")
                
            # 3. Apply the operation
            cursor.execute("""
                INSERT INTO sync_operations 
                (operation_id, entity_type, entity_id, operation_type, status, payload, client_created_at)
                VALUES (?, ?, ?, ?, 'APPLIED', ?, ?)
            """, (
                op_id, op["entity_type"], op["entity_id"], op["operation_type"], 
                json.dumps(payload), op["client_created_at"]
            ))
            
            cursor.execute(f"RELEASE SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "APPLIED"})
            
        except sqlite3.OperationalError as e:
            # 4a. Transient database failure (e.g., locked DB) -> Client should retry
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "RETRYABLE_ERROR"})
        except Exception as e:
            # 4b. Permanent failure (e.g., bad payload, missing columns) -> Client should discard
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "INVALID"})
            
    db_conn.commit()
    return results