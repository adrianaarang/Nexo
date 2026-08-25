// Renders active official alerts (Group 2).
// Handled states: loading, error, and empty (D2). Filters reload the list (D3).
import { getAlerts } from "./alertsApi.js";
import { crearTarjeta } from "../../shared/components/card.js";
import { el, formatDate } from "../../shared/utils.js";

const TYPE_LABELS = {
  terremoto: "Terremoto",
  ciclon: "Ciclón",
  inundacion: "Inundación",
  incendio: "Incendio",
  volcan: "Volcán",
  sequia: "Sequía",
  otro: "Otro",
  // English fallbacks in case backend sends English keys
  earthquake: "Terremoto",
  cyclone: "Ciclón",
  flood: "Inundación",
  fire: "Incendio",
  volcano: "Volcán",
  drought: "Sequía",
  other: "Otro",
};

const SEVERITY_LABELS = {
  red: "Crítico",
  orange: "Atención",
  green: "Bajo riesgo",
};

const SOURCES = ["GDACS"];

function getContainer() {
  return document.getElementById("alerts-container");
}

export function readFilters() {
  return {
    tipo: document.getElementById("type-filter")?.value ?? "",
    severidad: document.getElementById("severity-filter")?.value ?? "",
    pais: document.getElementById("country-filter")?.value.trim() ?? "",
  };
}

function updateMeta(lastUpdate) {
  return [
    el("p", {
      class: "alerts-meta__line",
      text: `Última actualización: ${formatDate(lastUpdate)}`,
    }),
    el("p", {
      class: "alerts-meta__line",
      text: `Fuentes consultadas: ${SOURCES.join(", ")}`,
    }),
  ];
}

export function renderAlert(alert) {
  const severidad = alert.severidad ?? alert.severity;
  const tipo = alert.tipo ?? alert.type;
  const pais = alert.pais ?? alert.country;
  const fecha = alert.fecha ?? alert.date;
  const descripcion = alert.descripcion ?? alert.description;
  const titulo = alert.titulo ?? alert.title;
  const enlace = alert.enlace ?? alert.link;

  const badge = {
    tipo: severidad,
    texto: SEVERITY_LABELS[severidad] ?? severidad,
  };

  const lines = [
    `${TYPE_LABELS[tipo] ?? tipo} · ${pais || "País desconocido"}`,
    formatDate(fecha),
  ];
  if (descripcion) lines.push(descripcion);

  const card = crearTarjeta({ titulo, lineas: lines, badge });

  if (enlace) {
    card.appendChild(
      el("a", {
        class: "nexo-btn nexo-btn--secondary alerts-link",
        href: enlace,
        target: "_blank",
        rel: "noopener",
        text: "Ver en GDACS",
      })
    );
  }
  return card;
}

export function renderList(alerts, lastUpdate) {
  getContainer().replaceChildren(
    el("div", { class: "alerts-meta" }, updateMeta(lastUpdate)),
    ...alerts.map(renderAlert)
  );
}

export function showEmptyState(lastUpdate) {
  getContainer().replaceChildren(
    el("h2", { class: "alerts-empty__title", text: "Sin alertas activas ahora" }),
    ...updateMeta(lastUpdate)
  );
}

export function showLoading() {
  getContainer().replaceChildren(
    el("p", { class: "alerts-state", text: "Cargando alertas…" })
  );
}

export function showError() {
  const retryButton = el("button", {
    class: "nexo-btn nexo-btn--secondary",
    type: "button",
    text: "Reintentar",
  });
  retryButton.addEventListener("click", fetchAlerts);

  getContainer().replaceChildren(
    el("h2", {
      class: "alerts-empty__title",
      text: "No se pudieron cargar las alertas",
    }),
    el("p", {
      class: "alerts-meta__line",
      text: "Comprueba tu conexión o inténtalo de nuevo.",
    }),
    retryButton
  );
}

export async function fetchAlerts() {
  showLoading();
  const lastUpdate = new Date().toISOString();

  try {
    const alerts = await getAlerts(readFilters());
    if (!alerts || !alerts.length) showEmptyState(lastUpdate);
    else renderList(alerts, lastUpdate);
  } catch (err) {
    console.error("Error loading alerts:", err);
    showError();
  }
}

export function initAlerts() {
  const form = document.getElementById("alerts-filters");
  form?.addEventListener("submit", (e) => {
    e.preventDefault();
    fetchAlerts();
  });

  ["type-filter", "severity-filter"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", fetchAlerts);
  });

  fetchAlerts();
}

document.addEventListener("DOMContentLoaded", initAlerts);
