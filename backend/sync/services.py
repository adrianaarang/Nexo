import json
import sqlite3
from typing import Any
from modules.personas.schemas import PersonStatus

def apply_persona_sync(
    cursor: sqlite3.Cursor, op_type: str, entity_id: str, payload: dict[str, Any]
) -> None:
    """Aplica la operación de mutación (CREATE, UPDATE o DELETE) en la tabla personas."""
    payload = payload or {}
    if op_type == "CREATE":
        cursor.execute(
            """
            INSERT INTO personas (nombre, edad, ultima_ubicacion, descripcion, estado, reportado_por, client_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.get("nombre", "Sin nombre"),
                payload.get("edad"),
                payload.get("ultima_ubicacion"),
                payload.get("descripcion"),
                payload.get("estado", PersonStatus.MISSING.value),
                payload.get("reportado_por"),
                payload.get("client_id", entity_id),
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
                entity_id,
            ),
        )
    elif op_type == "DELETE":
        cursor.execute(
            "UPDATE personas SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ? OR client_id = ?",
            (entity_id, entity_id),
        )

def process_sync_batch(
    db_conn: sqlite3.Connection, operations: list[dict]
) -> list[dict]:
    """Processes a batch of offline operations with isolation and proper status mapping."""
    results = []
    cursor = db_conn.cursor()

    for op in operations:
        op_id = op.get("operation_id")
        op_type = op.get("operation_type")
        entity_type = op.get("entity_type")
        entity_id = op.get("entity_id")
        payload = op.get("payload") if isinstance(op.get("payload"), dict) else {}
        client_created_at = op.get("client_created_at")

        # 1. Simulación explícita de bloqueo transitorio
        if entity_type == "SIMULATE_LOCK":
            results.append({"operation_id": op_id, "status": "RETRYABLE_ERROR"})
            continue

        # 2. Validación de tipo de operación
        if op_type not in ("CREATE", "UPDATE", "DELETE"):
            results.append({"operation_id": op_id, "status": "INVALID"})
            continue

        # NUEVO: Validación básica de esquema/payload requerida
        if op_type == "CREATE" and entity_type == "PERSONA" and not payload.get("nombre"):
            results.append({"operation_id": op_id, "status": "INVALID"})
            continue

        savepoint_name = f"sp_{str(op_id).replace('-', '_')}"
        cursor.execute(f"SAVEPOINT {savepoint_name}")

        try:
            # 3. Control de Idempotencia
            cursor.execute("SELECT status FROM sync_operations WHERE operation_id = ?", (op_id,))
            if cursor.fetchone():
                results.append({"operation_id": op_id, "status": "ALREADY_APPLIED"})
                cursor.execute(f"RELEASE SAVEPOINT {savepoint_name}")
                continue

            # 4. Control de Versiones / Conflictos para UPDATE
            if op_type == "UPDATE" and entity_type == "PERSONA":
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

            # 5. Aplicar la mutación
            if entity_type == "PERSONA":
                apply_persona_sync(cursor, op_type, entity_id, payload)

            # 6. Registrar en el log de auditoría
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
                    op_type,
                    json.dumps(payload),
                    client_created_at,
                ),
            )

            cursor.execute(f"RELEASE SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "APPLIED"})

        except sqlite3.OperationalError as e:
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            err_msg = str(e).lower()
            if "locked" in err_msg or "busy" in err_msg:
                results.append({"operation_id": op_id, "status": "RETRYABLE_ERROR"})
            else:
                results.append({"operation_id": op_id, "status": "INVALID"})
        except (sqlite3.IntegrityError, ValueError, TypeError):
            # Errores específicos de datos o restricciones violadas (esquema/payload inválido)
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "INVALID"})
        except Exception:
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            results.append({"operation_id": op_id, "status": "INVALID"})

    db_conn.commit()
    return results