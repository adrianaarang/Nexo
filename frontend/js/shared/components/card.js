// Tarjeta genérica reutilizada por varios módulos — parte de la base común.
import { el } from "../utils.js";

export function crearTarjeta({ titulo, lineas = [], badge }) {
  const card = el("div", { class: "nexo-card" });
  const h3 = el("h3", { text: titulo });
  if (badge) {
    const badgeEl = el("span", {
      class: `nexo-badge nexo-badge--${badge.tipo}`,
      text: badge.texto,
    });
    h3.appendChild(document.createTextNode(" "));
    h3.appendChild(badgeEl);
  }
  card.appendChild(h3);
  lineas.forEach((linea) => {
    card.appendChild(el("p", { class: "nexo-card__meta", text: linea }));
  });
  return card;
}
