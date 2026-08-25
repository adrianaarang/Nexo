import json
import sqlite3
from typing import Any

def apply_persona_sync(
    cursor: sqlite3.Cursor, op_type: str, entity_id: str, payload: dict[str, Any]
) -> None:

    """Aplica la operación de mutación (CREATE, UPDATE o DELETE) en la tabla personas."""
    if op_type == "CREATE":
        cursor.execute(
            """
            INSERT INTO personas (nombre, edad, ultima_ubicacion, descripcion, estado, reportado_por, client_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            (
                payload.get("nombre"),
                payload.get("edad"),
                payload.get("ultima_ubicacion"),
                payload.get("descripcion"),
                payload.get("estado", PersonStatus.MISSING.value),
                payload.get("reportado_por"),
                payload.get("client_id"),
            ),
        )
    elif op_type == "UPDATE":
        cursor.execute(
            """
            UPDATE personas
            SET nombre = COALESCE(?, nombre),
                estado = COALESCE(?, estado),
                ultima_ubicacion = COALESCE(?, ultima_ubicacion),
                version = version + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? OR client_id = ?
            """,
            (
                payload.get("nombre"),
                payload.get("estado"),
                payload.get("ultima_ubicacion"),
                entity_id,
                entity_id
            ),
        )
    elif op_type == "DELETE":
        cursor.execute(
            "UPDATE personas SET is_deleted = 1, updated_at CURRENT_TIMESTAMP WHERE id = ? OR client_id = ?",
            (entity_id, entity_id),
        )

def process_sync_batch(
    db_conn: sqlite3.Connection, operations: list[dict]
    ) -> list[dict]:
    """
    Processes a batch of offline operations. 
    Enforces idempotency, conflicts, and distinguishes retryable errors.
    """
    results = []
    cursor = db_conn.cursor()
    
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

            payload = op.get("payload", {})
            entity_type = op.get("entity_type")
            entity_id = op.get("entity_id")
                
            # Artificial trigger for testing temporary failures
            if entity_type == "SIMULATE_LOCK":
                raise sqlite3.OperationalError("database is locked")
                
            # 2. Concurrency Control (Stale version detection)
            if op["operation_type"] == "UPDATE" and entity_type == "PERSONA":
                cursor.execute(
                    "SELECT version FROM personas WHERE id = ? OR client_id = ?",
                    (entity_id, entity_id),
                )
                row = cursor.fetchone()
                if row:
                    server_version = row[0]
                    client_version = payload.get("version", 1)
                    if client_version < server_version:
                        results.append({"operation_id": op_id, "status": "CONFLICT"})
                        cursor.execute(f"RELEASE SAVEPOINT {savepoint_name}")
                        continue

            # 3. Apply database mutation
            if entity_type == "PERSONA":
                apply_persona_sync(cursor, op["operation_type"], entity_id, payload)

            # 4. Record operation in the audit log
            cursor.execute(
                """
                INSERT INTO sync_operations 
                (operation_id, entity_type, entity_id, operation_type, status, payload, client_created_at)
                VALUES (?, ?, ?, ?, 'APPLIED', ?, ?)
                """,
                (
                    op_id,
                    entity_type,
                    entity_id,
                    op["operation_type"],
                    json.dumps(payload),
                    op["client_created_at"],
                ),
            )

            cursor.execute(f"RELEASE SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "APPLIED"})

        except sqlite3.OperationalError:
            # Temporary database error (retryable by client)
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "RETRYABLE_ERROR"})
        except Exception:
            # Permanent error (invalid payload or query)
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "INVALID"})

    db_conn.commit()
    return results