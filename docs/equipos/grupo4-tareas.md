# Grupo 4 (Mapa + Interfaz principal) — Distribución de tareas (Sprint 2)

Reparto del equipo 4 recibido de Isabela (SM del grupo 4, `Isabela-Tellez`). En Sprint 2 el
**mapa** se mueve del Equipo 1 a este equipo, que además asume la **interfaz principal** de la app.

## A. Reparto por persona
- [ ] **Isabela (SM) — Coordinación de consumo de contratos**: alertas y necesidades, y resaltado de zona ALTO RIESGO.
- [ ] **Anas — Mapa** (`mapaNecesidades.js` + Leaflet): marcadores de necesidades (color por intensidad), marcadores de alertas y popups.
- [ ] **Eli — Consumo de alertas** (`alertasApi.js` / `crisis.js`): pintar la zona de la alerta, badge `risk_level`/`status`, y resaltado de ALTO RIESGO.
- [ ] **Yohanna — Interfaz principal / navegación**: menú, pantallas, estados de carga / vacío / error.
- [ ] **David — Intensidad y QA**: conteo 🟢🟠🔴 y tests de integración mapa ↔ alertas ↔ necesidades.

## B. Coordinación y dependencias
- Consume los contratos: alertas `{id, risk_level, status, zone}` (G2) y necesidades `{id, type, latitude, longitude, status}` (G1).
- Al activarse **ALTO RIESGO** se resalta la `zone` en el mapa y se desbloquean necesidades/ayudas en ella (coordina con G2).
- El backend de alertas/necesidades lo implementan G2/G1; G4 solo consume vía API (`apiClient.js`).

## C. Definition of Done (recordatorio)
Implementado · JS tests verdes · no rompe otros módulos · revisado en PR · demostrable en demo.
