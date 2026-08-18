# Nexo — Estructura de carpetas y archivos (HTML/CSS/JS + Python)

Basada en los votos del grupo: núcleo (Recurso integral, emergencia pura) → siguientes prioridades → futuro/roadmap.

```
nexo/
├── README.md
├── LICENSE                                 # futuro: código abierto
├── CONTRIBUTING.md                         # futuro: código abierto
├── .gitignore
├── .env.example
│
├── .github/
│   └── workflows/
│       └── ci.yml                          # lint + tests en cada push
│
├── frontend/
│   ├── index.html                          # pantalla principal (mapa)
│   ├── manifest.json                       # PWA — necesario para modo offline
│   │
│   ├── pages/
│   │   ├── mapa.html
│   │   ├── alertas.html
│   │   ├── voluntariado.html
│   │   ├── donaciones.html
│   │   ├── personas.html
│   │   └── estoy-bien.html
│   │
│   ├── css/
│   │   ├── variables.css                   # colores, tipografía de marca Nexo
│   │   ├── style.css                       # base
│   │   └── components.css
│   │
│   ├── js/
│   │   ├── app.js                          # arranque, router simple
│   │   │
│   │   ├── core/                                   # ── NÚCLEO (MVP) ──
│   │   │   ├── mapa-necesidades/
│   │   │   │   ├── mapaNecesidades.js
│   │   │   │   ├── necesidadCard.js
│   │   │   │   └── necesidadesApi.js
│   │   │   ├── alertas-oficiales/
│   │   │   │   ├── alertas.js
│   │   │   │   └── alertasApi.js
│   │   │   └── voluntariado-donaciones/
│   │   │       ├── voluntariado.js
│   │   │       ├── donaciones.js
│   │   │       └── voluntariadoApi.js
│   │   │
│   │   ├── siguiente/                               # ── SIGUIENTES PRIORIDADES ──
│   │   │   ├── registro-personas/
│   │   │   │   ├── registroPersonas.js
│   │   │   │   ├── estoyBien.js
│   │   │   │   └── personasApi.js
│   │   │   └── modo-offline/
│   │   │       ├── localDb.js               # wrapper IndexedDB
│   │   │       ├── syncQueue.js
│   │   │       └── serviceWorker.js
│   │   │
│   │   ├── futuro/                                   # ── ROADMAP (no MVP) ──
│   │   │   ├── red-mesh-satelite/
│   │   │   │   └── README.md
│   │   │   └── codigo-abierto/
│   │   │       └── README.md
│   │   │
│   │   └── shared/
│   │       ├── apiClient.js                  # fetch centralizado
│   │       ├── utils.js
│   │       └── components/
│   │           ├── header.js
│   │           └── card.js
│   │
│   └── assets/
│       ├── logo/
│       │   ├── nexo-logo.png
│       │   └── nexo-icon.png
│       ├── icons/
│       └── images/
│
├── backend/
│   ├── requirements.txt
│   ├── main.py                              # entrypoint FastAPI
│   ├── config.py
│   ├── .env.example
│   │
│   ├── modules/                                     # ── NÚCLEO ──
│   │   ├── necesidades/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── alertas/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── services.py                   # llama a integrations/gdacs_client.py
│   │   ├── voluntariado/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── donaciones/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── models.py
│   │   │
│   │   └── personas/                          # ── SIGUIENTE ──
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       ├── models.py
│   │       └── schemas.py
│   │
│   ├── integrations/
│   │   ├── gdacs_client.py                    # alertas globales (ONU/UE) — fuente principal
│   │   └── proteccion_civil_client.py         # capa local opcional (detalle fino en España)
│   │
│   ├── sync/                                  # ── SIGUIENTE ──
│   │   └── sync_controller.py                 # resuelve conflictos offline
│   │
│   ├── middleware/
│   │   ├── auth.py
│   │   └── error_handler.py
│   │
│   └── db/
│       ├── database.py
│       ├── migrations/
│       │   └── 001_init.sql
│       └── seed.py                            # datos de ejemplo para demo
│
├── infra/
│   └── mesh-satelite/                          # ── FUTURO ──
│       ├── README.md
│       └── notas-tecnicas.md
│
├── tests/
│   ├── frontend/
│   │   └── mapa-necesidades.test.js
│   └── backend/
│       └── test_necesidades.py
│
└── docs/
    ├── decisiones-encuesta.md                  # resumen de por qué este alcance
    ├── roadmap.md                              # núcleo → siguiente → futuro
    ├── architecture.md
    └── privacidad-datos.md                     # tratamiento de ubicación y datos sensibles
```

## Notas

- **Alertas a nivel mundial**: el módulo `alertas` usa GDACS (Global Disaster Alert and Coordination System, ONU/Comisión Europea) como fuente principal — cubre terremotos, inundaciones, ciclones, etc. en cualquier país con feeds gratuitos. Protección Civil se mantiene como capa local opcional para más detalle dentro de España. AEMET queda descartado del núcleo (solo aporta previsión meteorológica, no encaja con el eje de "emergencia pura" que votó el grupo).
- **`manifest.json` + `serviceWorker.js`**: sin un framework, la forma estándar de conseguir "modo offline" real en web es convertir el frontend en PWA (Progressive Web App) — cachea la app y permite guardar datos con IndexedDB (`localDb.js`) aunque no haya red.
- **`apiClient.js`**: un único punto donde todas las llamadas `fetch()` pasan, para poder interceptar y encolar peticiones en `syncQueue.js` cuando no hay conexión.
- **Backend con FastAPI**: cada módulo (`necesidades`, `alertas`, `voluntariado`...) es autocontenido con sus propias rutas, modelos y schemas — fácil de repartir entre miembros del equipo sin pisarse el código.
- **`privacidad-datos.md`**: sigue siendo necesario — la app maneja ubicación en tiempo real y datos de personas desaparecidas.
- **`db/seed.py`**: datos ficticios (necesidades, alertas, voluntarios) para poder enseñar la app funcionando en la demo.
