// Service worker (Equipo 4, siguiente prioridad).
// Versión mínima de la base común: no cachea nada todavía, pero existe
// para que app.js pueda registrarlo sin error 404.
// TODO (Equipo 4): cachear el app shell (HTML/CSS/JS/logo) para que
// Nexo cargue sin conexión.

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", () => self.clients.claim());
