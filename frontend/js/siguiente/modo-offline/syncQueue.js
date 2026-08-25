// Cola de sincronización (Equipo 4, siguiente prioridad).
//
// Versión mínima de la base común: no rompe al resto de módulos
// (js/shared/apiClient.js depende de estas dos funciones), pero de
// momento no guarda nada de verdad.
//
// TODO (Equipo 4): usar localDb.js (IndexedDB) para guardar de verdad
// las acciones pendientes en encolarAccion(), y en procesarColaPendiente()
// leerlas, enviarlas a POST /api/sync, y vaciar la cola si sale bien.

export async function encolarAccion(modulo, payload) {
  console.warn(`Nexo: sin conexión y sin cola offline implementada todavía (${modulo}).`, payload);
}

export async function procesarColaPendiente() {
  // TODO (Equipo 4): implementar.
}
