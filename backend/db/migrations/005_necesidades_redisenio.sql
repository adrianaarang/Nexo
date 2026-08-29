-- Migra instalaciones anteriores al contrato de ocho categorías y dos estados.
-- SQLite no permite modificar un CHECK existente, por lo que se reconstruye la
-- tabla y se transforman los valores antiguos sin perder identificadores.

CREATE TABLE necesidades_nueva (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL DEFAULT '',
    tipo TEXT NOT NULL CHECK (
        tipo IN (
            'agua', 'alimentos', 'parafarmacia', 'ropa',
            'higiene', 'refugio', 'transporte', 'otros'
        )
    ),
    descripcion TEXT NOT NULL DEFAULT '',
    direccion TEXT NOT NULL DEFAULT '',
    latitud REAL NOT NULL,
    longitud REAL NOT NULL,
    prioridad TEXT NOT NULL DEFAULT 'media' CHECK (
        prioridad IN ('baja', 'media', 'alta', 'critica')
    ),
    estado TEXT NOT NULL DEFAULT 'abierta' CHECK (
        estado IN ('abierta', 'cubierta')
    ),
    creado_en TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

INSERT INTO necesidades_nueva (
    id, titulo, tipo, descripcion, direccion, latitud, longitud,
    prioridad, estado, creado_en
)
SELECT
    id,
    titulo,
    CASE tipo
        WHEN 'alimento' THEN 'alimentos'
        WHEN 'medicina' THEN 'parafarmacia'
        WHEN 'herramientas' THEN 'otros'
        WHEN 'agua' THEN 'agua'
        WHEN 'alimentos' THEN 'alimentos'
        WHEN 'parafarmacia' THEN 'parafarmacia'
        WHEN 'ropa' THEN 'ropa'
        WHEN 'higiene' THEN 'higiene'
        WHEN 'refugio' THEN 'refugio'
        WHEN 'transporte' THEN 'transporte'
        ELSE 'otros'
    END,
    descripcion,
    direccion,
    latitud,
    longitud,
    prioridad,
    CASE estado
        WHEN 'cubierta' THEN 'cubierta'
        ELSE 'abierta'
    END,
    creado_en
FROM necesidades;

DROP TABLE necesidades;
ALTER TABLE necesidades_nueva RENAME TO necesidades;
