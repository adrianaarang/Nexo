-- Esquema inicial de Nexo — módulos del núcleo y de siguiente prioridad.
-- Parte de la base común: cada equipo usa estas tablas desde su módulo,
-- nadie necesita tocar este archivo salvo que cambie el modelo de datos.

CREATE TABLE IF NOT EXISTS necesidades (
    -- Se mantiene INTEGER porque el contrato admite UUID o entero y el MVP
    -- ya utiliza el autoincremento de SQLite.
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    -- CHECK replica los valores cerrados de schemas.py también en persistencia.
    tipo TEXT NOT NULL CHECK (
        tipo IN (
            'agua', 'alimento', 'medicina', 'refugio',
            'herramientas', 'transporte'
        )
    ),
    descripcion TEXT NOT NULL,
    -- La validación precisa de rangos se realiza en Pydantic antes del INSERT.
    latitud REAL NOT NULL,
    longitud REAL NOT NULL,
    prioridad TEXT NOT NULL DEFAULT 'media' CHECK (
        prioridad IN ('baja', 'media', 'alta', 'critica')
    ),
    estado TEXT NOT NULL DEFAULT 'abierta' CHECK (
        estado IN ('abierta', 'en_proceso', 'cubierta')
    ),
    -- Formato ISO 8601 UTC compatible con el sufijo Z del contrato JSON.
    creado_en TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS voluntarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    contacto TEXT NOT NULL,
    habilidades TEXT NOT NULL DEFAULT '',
    disponibilidad TEXT NOT NULL DEFAULT 'inmediata',
    creado_en TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS donaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,               -- ofrecida, solicitada
    recurso TEXT NOT NULL,
    cantidad TEXT NOT NULL DEFAULT '',
    contacto TEXT NOT NULL,
    creado_en TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    -- Estados admitidos: desaparecida, localizada, estoy_bien.
    estado TEXT NOT NULL DEFAULT 'desaparecida',
    ultima_ubicacion TEXT NOT NULL DEFAULT '',
    reportado_por TEXT NOT NULL DEFAULT '',
    creado_en TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modulo TEXT NOT NULL,
    accion TEXT NOT NULL,
    payload TEXT NOT NULL,
    procesado_en TEXT NOT NULL DEFAULT (datetime('now'))
);
