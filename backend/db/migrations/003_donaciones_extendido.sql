ALTER TABLE donaciones ADD COLUMN descripcion TEXT NOT NULL DEFAULT '';

ALTER TABLE donaciones ADD COLUMN estado TEXT NOT NULL DEFAULT 'activa'
    CHECK (estado IN ('activa', 'entregada'));