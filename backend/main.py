"""Punto de arranque del backend de Nexo (FastAPI).

Parte de la base común: registra los routers de cada módulo, CORS y
manejo de errores. Los equipos NO deberían tener que tocar este
archivo salvo para registrar un router nuevo si crean un módulo.

uvicorn main:app --reload --port 8000
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Obtener la ruta del directorio base del Backend
BASE_DIR = Path(__file__).resolve().parent

# Inicializar la configuración de logs antes de importar otros módulos 
from middleware.logging_config import setup_logging

setup_logging()

from config import CORS_ORIGINS
from db.database import init_db
from middleware.error_handler import registrar_manejadores_de_error

from modules.necesidades.routes import router as necesidades_router
from modules.alertas.routes import router as alertas_router
from modules.voluntariado.routes import router as voluntariado_router
from modules.donaciones.routes import router as donaciones_router
from modules.personas.routes import router as personas_router
from sync.sync_controller import router as sync_router

app = FastAPI(
    title="Nexo API",
    description="Conectados para ayudarnos — respuesta a emergencias y desastres.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

registrar_manejadores_de_error(app)

app.include_router(necesidades_router)     # Equipo 1 — núcleo
app.include_router(alertas_router)         # Equipo 2 — núcleo
app.include_router(voluntariado_router)    # Equipo 3 — núcleo
app.include_router(donaciones_router)      # Equipo 3 — núcleo
app.include_router(personas_router)        # Equipo 4 — siguiente prioridad
app.include_router(sync_router)            # Equipo 4 — siguiente prioridad (modo offline)

# Inicializar la base de datos (ejecuta esquemas y migraciones automáticamente)
init_db()

@app.get("/api/health")
def health():
    """Si esto responde, la base común está bien montada."""
    return {"status": "ok", "app": "Nexo"}