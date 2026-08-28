-- Añade la columna "direccion" a necesidades para quien ya tenía la tabla
-- creada antes de este rediseño (CREATE TABLE IF NOT EXISTS de 001_init.sql
-- no toca tablas ya existentes). En una base de datos nueva esta columna ya
-- viene incluida en 001_init.sql y este ALTER falla con "duplicate column",
-- error que database.py ignora a propósito para que las migraciones sean
-- idempotentes (ver _run_migration en db/database.py).
ALTER TABLE necesidades ADD COLUMN direccion TEXT NOT NULL DEFAULT '';
