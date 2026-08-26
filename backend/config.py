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

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500").split(",")

GDACS_API_URL = os.getenv("GDACS_API_URL", "https://www.gdacs.org/xml/rss.xml")
GDACS_CACHE_TTL_SECONDS = int(os.getenv("GDACS_CACHE_TTL_SECONDS", "900"))
PROTECCION_CIVIL_API_URL = os.getenv("PROTECCION_CIVIL_API_URL", "")
GDACS_CACHE_TTL_SECONDS = int(os.getenv("GDACS_CACHE_TTL_SECONDS", "900"))

# Voluntariado: correo, admin y subida de archivos
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@nexo-dummy.local")
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "nexo@dummy.local")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "dummy-password")
EMAIL_DUMMY_MODE = os.getenv("EMAIL_DUMMY_MODE", "true").lower() == "true"
NEXO_ADMIN_KEY = os.getenv("NEXO_ADMIN_KEY", "nexo-dev-admin-key")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/voluntarios")
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "5"))
