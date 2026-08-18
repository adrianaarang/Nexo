# Cómo contribuir a Nexo

Este documento se activa en la fase de código abierto (roadmap futuro). Por ahora,
para el equipo del proyecto:

1. Crea una rama por funcionalidad: `feature/mapa-necesidades`, `fix/sync-offline`...
2. Un módulo = una carpeta autocontenida (ver `docs/architecture.md`). Evita tocar
   módulos de otras personas sin avisar.
3. Antes de subir un cambio al backend, ejecuta `pytest` dentro de `backend/`.
4. Describe en el commit qué prioridad afecta: núcleo, siguiente o futuro.
5. Abre un pull request pequeño y descriptivo; evita mezclar varios módulos en uno.
