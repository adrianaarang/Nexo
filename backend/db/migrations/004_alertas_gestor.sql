-- Alertas creadas por el gestor (Equipo 2): activación de crisis y nivel de riesgo.
-- Se añade una tabla propia, independiente de las alertas externas (GDACS /
-- Protección Civil) que se siguen obteniendo en vivo desde los integrations.

CREATE TABLE IF NOT EXISTS alertas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- nivel_riesgo replica los valores cerrados de schemas.RiskLevelEnum también en BD.
    nivel_riesgo TEXT NOT NULL CHECK (nivel_riesgo IN ('bajo', 'medio', 'alto')),
    -- zona se guarda como GeoJSON Polygon serializado en texto (MVP sin PostGIS).
    zona TEXT NOT NULL,
    -- activa: 0 = inactiva (normal), 1 = activa. ALTO RIESGO además fija nivel_riesgo='alto'.
    activa INTEGER NOT NULL DEFAULT 0 CHECK (activa IN (0, 1)),
    -- gestor_token identifica al gestor que creó/activó la alerta (MVP sin login).
    gestor_token TEXT NOT NULL,
    titulo TEXT NOT NULL DEFAULT '',
    descripcion TEXT NOT NULL DEFAULT '',
    -- tipo es opcional y reusa EventTypeEnum cuando el gestor lo indica.
    tipo TEXT,
    fuente TEXT NOT NULL DEFAULT 'gestor',
    latitud REAL,
    longitud REAL,
    creado_en TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
