// La cabecera ya está en cada página como HTML estático (ver
// frontend/pages/*.html) para que funcione sin JavaScript. Parte de la
// base común — este archivo solo marca qué enlace del menú está activo.
export function marcarPaginaActiva() {
  const actual = window.location.pathname.split("/").pop();
  document.querySelectorAll(".nexo-nav a").forEach((link) => {
    if (link.getAttribute("href") === actual) {
      link.setAttribute("aria-current", "page");
    }
  });
}
