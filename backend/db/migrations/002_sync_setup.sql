
--Sync Operation which we can track operation_id like timestamp UUID, server timestamp,etc..
CREATE TABLE IF NOT EXISTS sync_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_id TEXT NOT NULL UNIQUE,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    operation_type TEXT NOT NULL CHECK (operation_type IN ('CREATE', 'UPDATE', 'DELETE')),
    status TEXT NOT NULL CHECK (status IN ('PENDING', 'APPLIED', 'ALREADY_APPLIED', 'CONFLICT', 'INVALID', 'RETRYABLE_ERROR')),
    payload TEXT NOT NULL, -- JSON string
    client_created_at TEXT NOT NULL,
    server_processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_code TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimizar la búsqueda frecuente por ID de operación y entidad
CREATE INDEX IF NOT EXISTS idx_sync_operations_op_id ON sync_operations(operation_id);
CREATE INDEX IF NOT EXISTS idx_sync_operations_entity ON sync_operations(entity_type, entity_id);