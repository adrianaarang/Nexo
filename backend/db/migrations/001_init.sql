-- Esquema inicial de Nexo — módulos del núcleo y de siguiente prioridad.
-- Parte de la base común: cada equipo usa estas tablas desde su módulo,
-- nadie necesita tocar este archivo salvo que cambie el modelo de datos.

CREATE TABLE IF NOT EXISTS necesidades (
    -- Se mantiene INTEGER porque el contrato admite UUID o entero y el MVP
    -- ya utiliza el autoincremento de SQLite.
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Opcional: si el formulario simplificado no lo rellena, el servicio
    -- (services.py) genera uno a partir de la categoría antes de guardar.
    titulo TEXT NOT NULL DEFAULT '',
    -- CHECK replica los valores cerrados de schemas.py también en persistencia.
    -- Rediseño del Equipo 1: 8 categorías cerradas (antes 6).
    tipo TEXT NOT NULL CHECK (
        tipo IN (
            'agua', 'alimentos', 'parafarmacia', 'ropa',
            'higiene', 'refugio', 'transporte', 'otros'
        )
    ),
    -- Opcional: el formulario simplificado no la exige (ver schemas.py).
    descripcion TEXT NOT NULL DEFAULT '',
    -- Texto legible del lugar (p. ej. "Calle Mayor 3, Valencia"), obtenido
    -- por geocodificación en el frontend (ver geocodificacion.js). Las
    -- coordenadas de abajo son las que usa el mapa: esta columna es solo
    -- para mostrar algo legible en la tarjeta y el popup.
    direccion TEXT NOT NULL DEFAULT '',
    -- La validación precisa de rangos se realiza en Pydantic antes del INSERT.
    latitud REAL NOT NULL,
    longitud REAL NOT NULL,
    prioridad TEXT NOT NULL DEFAULT 'media' CHECK (
        prioridad IN ('baja', 'media', 'alta', 'critica')
    ),
    -- Rediseño del Equipo 1: ciclo de vida a un solo paso (antes había
    -- un estado intermedio "en_proceso" que se ha retirado).
    estado TEXT NOT NULL DEFAULT 'abierta' CHECK (
        estado IN ('abierta', 'cubierta')
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
