-- Esquema inicial de Nexo — módulos del núcleo y de siguiente prioridad.
-- Parte de la base común: cada equipo usa estas tablas desde su módulo,
-- nadie necesita tocar este archivo salvo que cambie el modelo de datos.

CREATE TABLE IF NOT EXISTS necesidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,              -- agua, comida, refugio, medicinas, otro
    descripcion TEXT NOT NULL,
    latitud REAL NOT NULL,
    longitud REAL NOT NULL,
    prioridad TEXT NOT NULL DEFAULT 'media',  -- alta, media, baja
    estado TEXT NOT NULL DEFAULT 'abierta',   -- abierta, en_proceso, cubierta
    creado_en TEXT NOT NULL DEFAULT (datetime('now'))
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
    estado TEXT NOT NULL DEFAULT 'desaparecida',  -- desaparecida, localizada, estoy_bien
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
