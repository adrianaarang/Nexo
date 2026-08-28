"""Conexión a la base de datos SQLite y utilidades básicas.

Se usa sqlite3 directamente (sin ORM) para mantener el proyecto simple
en esta fase de MVP. Si el proyecto crece, valorar SQLAlchemy.
"""
import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path

# Asegura que la raíz de backend/ está en el path, para que este módulo
# funcione tanto si se importa desde main.py como si se ejecuta suelto
# (por ejemplo `python db/seed.py`).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DATABASE_PATH

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()


def _run_migration(conn, sql):
    """Ejecuta un archivo de migración sentencia por sentencia.

    SQLite no admite `ADD COLUMN IF NOT EXISTS`, así que al re-ejecutar
    las migraciones en un arranque posterior los `ALTER TABLE` fallan con
    "duplicate column name". Esos errores son esperados e inofensivos: los
    ignoramos para que `init_db` sea idempotente.
    """
    for raw in sql.split(";"):
        statement = raw.strip()
        if not statement:
            continue
        try:
            conn.execute(statement)
        except sqlite3.OperationalError as err:
            message = str(err).lower()
            if "duplicate column" in message or "already exists" in message:
                continue
            raise


def init_db():
    """Ejecuta todas las migraciones .sql en orden. Idempotente:
    los `CREATE TABLE IF NOT EXISTS` no recrean tablas y los `ALTER TABLE`
    ya aplicados se ignoran (ver `_run_migration`)."""
    conn = get_connection()
    try:
        for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
            _run_migration(conn, migration.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()
