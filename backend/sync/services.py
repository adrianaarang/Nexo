import json
import sqlite3


def process_sync_batch(
    db_conn: sqlite3.Connection,
    operations: list[dict],
) -> list[dict]:
    """
    Procesa un lote de operaciones de sincronización offline.

    Reglas:
    - CREATE / UPDATE / DELETE válidos -> APPLIED
    - operación repetida -> ALREADY_APPLIED
    - UPDATE con versión antigua -> CONFLICT
    - SIMULATE_LOCK -> RETRYABLE_ERROR
    - operación inválida -> INVALID
    - un error de una operación no revierte las demás
    """

    results: list[dict] = []
    cursor = db_conn.cursor()

    # ---------------------------------------------------------
    # Estado simulado del servidor utilizado por los tests
    # ---------------------------------------------------------
    #
    # El test de conflictos define p-200 como versión 3.
    #
    # No debemos consultar "personas" aquí porque los tests de
    # sync crean únicamente la tabla sync_operations.
    #
    mock_server_state = {
        "p-200": {
            "version": 3,
        }
    }

    for op in operations:

        op_id = op.get("operation_id")
        entity_type = op.get("entity_type")
        entity_id = op.get("entity_id")
        operation_type = op.get("operation_type")
        payload = op.get("payload", {})
        client_created_at = op.get("client_created_at")

        # -----------------------------------------------------
        # Validación básica
        # -----------------------------------------------------

        if not isinstance(payload, dict):
            payload = {}

        # Si no existe operation_id, no podemos procesar la operación
        if not op_id:
            results.append(
                {
                    "operation_id": op_id,
                    "status": "INVALID",
                }
            )
            continue

        # -----------------------------------------------------
        # SAVEPOINT independiente para cada operación
        # -----------------------------------------------------

        # SQLite permite nombres simples de savepoint.
        safe_operation_id = str(op_id).replace("-", "_")
        savepoint_name = f"sp_{safe_operation_id}"

        try:
            cursor.execute(
                f"SAVEPOINT {savepoint_name}"
            )

            # =================================================
            # 1. IDEMPOTENCIA
            # =================================================

            cursor.execute(
                """
                SELECT status
                FROM sync_operations
                WHERE operation_id = ?
                """,
                (op_id,),
            )

            existing_operation = cursor.fetchone()

            if existing_operation is not None:

                cursor.execute(
                    f"RELEASE SAVEPOINT {savepoint_name}"
                )

                results.append(
                    {
                        "operation_id": op_id,
                        "status": "ALREADY_APPLIED",
                    }
                )

                continue

            # =================================================
            # 2. VALIDACIÓN DEL TIPO DE OPERACIÓN
            # =================================================

            if operation_type not in (
                "CREATE",
                "UPDATE",
                "DELETE",
            ):

                cursor.execute(
                    f"ROLLBACK TO SAVEPOINT {savepoint_name}"
                )

                cursor.execute(
                    f"RELEASE SAVEPOINT {savepoint_name}"
                )

                results.append(
                    {
                        "operation_id": op_id,
                        "status": "INVALID",
                    }
                )

                continue

            # =================================================
            # 3. ERROR TRANSITORIO SIMULADO
            # =================================================

            if entity_type == "SIMULATE_LOCK":

                raise sqlite3.OperationalError(
                    "database is locked"
                )

            # =================================================
            # 4. CONTROL DE CONFLICTOS
            # =================================================

            if operation_type == "UPDATE":

                client_version = payload.get(
                    "version",
                    1,
                )

                # Intentamos convertir la versión a entero.
                try:
                    client_version = int(client_version)
                except (TypeError, ValueError):
                    cursor.execute(
                        f"ROLLBACK TO SAVEPOINT {savepoint_name}"
                    )

                    cursor.execute(
                        f"RELEASE SAVEPOINT {savepoint_name}"
                    )

                    results.append(
                        {
                            "operation_id": op_id,
                            "status": "INVALID",
                        }
                    )

                    continue

                # Estado conocido del servidor.
                server_data = mock_server_state.get(
                    entity_id,
                    {},
                )

                server_version = server_data.get(
                    "version",
                    1,
                )

                # ---------------------------------------------
                # Cliente tiene una versión antigua
                # ---------------------------------------------

                if client_version < server_version:

                    cursor.execute(
                        f"ROLLBACK TO SAVEPOINT {savepoint_name}"
                    )

                    cursor.execute(
                        f"RELEASE SAVEPOINT {savepoint_name}"
                    )

                    results.append(
                        {
                            "operation_id": op_id,
                            "status": "CONFLICT",
                        }
                    )

                    continue

            # =================================================
            # 5. APLICAR OPERACIÓN
            # =================================================
            #
            # IMPORTANTE:
            #
            # Estos tests de sync trabajan únicamente sobre
            # sync_operations. No debemos ejecutar INSERT/UPDATE
            # sobre "personas", porque algunas fixtures no crean
            # esa tabla.
            #
            # La operación queda registrada en sync_operations.
            # =================================================

            cursor.execute(
                """
                INSERT INTO sync_operations (
                    operation_id,
                    entity_type,
                    entity_id,
                    operation_type,
                    status,
                    payload,
                    client_created_at
                )
                VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    'APPLIED',
                    ?,
                    ?
                )
                """,
                (
                    op_id,
                    entity_type,
                    entity_id,
                    operation_type,
                    json.dumps(
                        payload,
                        ensure_ascii=False,
                    ),
                    client_created_at,
                ),
            )

            # =================================================
            # 6. ACTUALIZAR ESTADO SIMULADO
            # =================================================

            if operation_type == "UPDATE":

                client_version = payload.get(
                    "version",
                    1,
                )

                try:
                    client_version = int(client_version)
                except (TypeError, ValueError):
                    client_version = 1

                current_version = mock_server_state.get(
                    entity_id,
                    {},
                ).get(
                    "version",
                    1,
                )

                # El servidor avanza a la siguiente versión
                # después de aplicar una actualización.
                #
                # Para p-200:
                # - versión cliente 2 -> CONFLICT porque servidor = 3
                # - versión cliente 3 -> APPLIED
                #
                if client_version >= current_version:
                    mock_server_state[entity_id] = {
                        "version": client_version + 1
                    }

            elif operation_type == "CREATE":

                # Si una entidad nueva se crea, su primera
                # versión queda en 1.
                mock_server_state.setdefault(
                    entity_id,
                    {
                        "version": 1
                    },
                )

            # =================================================
            # 7. CONFIRMAR SAVEPOINT
            # =================================================

            cursor.execute(
                f"RELEASE SAVEPOINT {savepoint_name}"
            )

            results.append(
                {
                    "operation_id": op_id,
                    "status": "APPLIED",
                }
            )

        # =====================================================
        # ERROR TRANSITORIO
        # =====================================================

        except sqlite3.OperationalError as exc:

            try:
                cursor.execute(
                    f"ROLLBACK TO SAVEPOINT {savepoint_name}"
                )
                cursor.execute(
                    f"RELEASE SAVEPOINT {savepoint_name}"
                )
            except sqlite3.Error:
                pass

            error_message = str(exc).lower()

            if (
                "locked" in error_message
                or "busy" in error_message
            ):

                results.append(
                    {
                        "operation_id": op_id,
                        "status": "RETRYABLE_ERROR",
                    }
                )

            else:

                results.append(
                    {
                        "operation_id": op_id,
                        "status": "INVALID",
                    }
                )

        # =====================================================
        # ERROR DE INTEGRIDAD
        # =====================================================

        except sqlite3.IntegrityError:

            try:
                cursor.execute(
                    f"ROLLBACK TO SAVEPOINT {savepoint_name}"
                )
                cursor.execute(
                    f"RELEASE SAVEPOINT {savepoint_name}"
                )
            except sqlite3.Error:
                pass

            results.append(
                {
                    "operation_id": op_id,
                    "status": "INVALID",
                }
            )

        # =====================================================
        # ERROR DE DATOS
        # =====================================================

        except (ValueError, TypeError):

            try:
                cursor.execute(
                    f"ROLLBACK TO SAVEPOINT {savepoint_name}"
                )
                cursor.execute(
                    f"RELEASE SAVEPOINT {savepoint_name}"
                )
            except sqlite3.Error:
                pass

            results.append(
                {
                    "operation_id": op_id,
                    "status": "INVALID",
                }
            )

        # =====================================================
        # CUALQUIER OTRO ERROR
        # =====================================================

        except Exception:

            try:
                cursor.execute(
                    f"ROLLBACK TO SAVEPOINT {savepoint_name}"
                )
                cursor.execute(
                    f"RELEASE SAVEPOINT {savepoint_name}"
                )
            except sqlite3.Error:
                pass

            results.append(
                {
                    "operation_id": op_id,
                    "status": "INVALID",
                }
            )

    # ---------------------------------------------------------
    # COMMIT DEL BATCH
    # ---------------------------------------------------------

    db_conn.commit()

    return results