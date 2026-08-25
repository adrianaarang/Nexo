-- Validación de voluntarios: estado, disponibilidad activa y documentos adjuntos.

ALTER TABLE voluntarios ADD COLUMN estado TEXT NOT NULL DEFAULT 'pendiente'
    CHECK (estado IN ('pendiente', 'aprobado', 'rechazado'));

ALTER TABLE voluntarios ADD COLUMN disponible INTEGER NOT NULL DEFAULT 0
    CHECK (disponible IN (0, 1));

ALTER TABLE voluntarios ADD COLUMN admin_token TEXT NOT NULL DEFAULT '';

ALTER TABLE voluntarios ADD COLUMN volunteer_token TEXT NOT NULL DEFAULT '';

CREATE TABLE IF NOT EXISTS voluntario_documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voluntario_id INTEGER NOT NULL,
    nombre_original TEXT NOT NULL,
    ruta TEXT NOT NULL,
    tipo_mime TEXT NOT NULL,
    creado_en TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (voluntario_id) REFERENCES voluntarios(id) ON DELETE CASCADE
);
