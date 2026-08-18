# Nexo — Conectados para ayudarnos

App comunitaria de respuesta a emergencias y desastres naturales: mapa de necesidades en tiempo real, alertas oficiales, voluntariado y donaciones. Registro de personas y modo sin conexión como siguientes prioridades. Red mesh/satélite y código abierto quedan como roadmap futuro.

Alcance decidido por votación de equipo — ver `docs/decisiones-encuesta.md` y `docs/roadmap.md`.

## Estructura

- `frontend/` — HTML, CSS y JS (PWA, sin framework).
- `backend/` — API en Python (FastAPI).
- `docs/` — decisiones de producto, arquitectura y privacidad.
- `infra/` — notas de infraestructura futura (red mesh/satélite).

## Cómo arrancar

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python db/seed.py               # datos de ejemplo
uvicorn main:app --reload --port 8000
```

La API queda disponible en `http://localhost:8000`. Documentación automática en `http://localhost:8000/docs`.

### Frontend

No necesita build. Sirve la carpeta `frontend/` con cualquier servidor estático, por ejemplo:

```bash
cd frontend
python -m http.server 5500
```

Abre `http://localhost:5500`. El frontend espera la API en `http://localhost:8000` (configurable en `frontend/js/shared/apiClient.js`).

## Módulos

| Prioridad | Módulo | Carpeta |
|---|---|---|
| Núcleo | Mapa de necesidades | `frontend/js/core/mapa-necesidades`, `backend/modules/necesidades` |
| Núcleo | Alertas oficiales (globales, GDACS) | `frontend/js/core/alertas-oficiales`, `backend/modules/alertas` |
| Núcleo | Voluntariado y donaciones | `frontend/js/core/voluntariado-donaciones`, `backend/modules/voluntariado`, `backend/modules/donaciones` |
| Siguiente | Registro de personas / estoy bien | `frontend/js/siguiente/registro-personas`, `backend/modules/personas` |
| Siguiente | Modo offline | `frontend/js/siguiente/modo-offline`, `backend/sync` |
| Futuro | Red mesh / satélite | `infra/mesh-satelite` |
| Futuro | Código abierto | `LICENSE`, `CONTRIBUTING.md` |
