// Arranque común a todas las páginas — parte de la base común: registra
// el service worker (PWA/offline) y muestra el aviso de "sin conexión".
import { marcarPaginaActiva } from "./shared/components/header.js";
import { procesarColaPendiente } from "./siguiente/modo-offline/syncQueue.js";

marcarPaginaActiva();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/js/siguiente/modo-offline/serviceWorker.js")
      .catch((err) => console.warn("No se pudo registrar el service worker:", err));
  });
}

function actualizarBannerOffline() {
  const banner = document.getElementById("nexo-offline-banner");
  if (!banner) return;
  banner.classList.toggle("visible", !navigator.onLine);
}

window.addEventListener("online", () => {
  actualizarBannerOffline();
  procesarColaPendiente();
});
window.addEventListener("offline", actualizarBannerOffline);
actualizarBannerOffline();

if (navigator.onLine) {
  procesarColaPendiente();
}
