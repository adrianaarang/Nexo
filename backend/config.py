"""Configuración general del backend de Nexo.

Lee variables de entorno (ver .env.example) con valores por defecto
razonables para desarrollo local.
"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nexo.db")
DATABASE_PATH = DATABASE_URL.replace("sqlite:///", "")

BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5500").split(",")

GDACS_API_URL = os.getenv("GDACS_API_URL", "https://www.gdacs.org/xml/rss.xml")
PROTECCION_CIVIL_API_URL = os.getenv("PROTECCION_CIVIL_API_URL", "")
