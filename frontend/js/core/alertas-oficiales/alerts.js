// Renders active official alerts (Group 2).
// Handled states: loading, error, and empty (D2). Filters reload the list (D3).
import { getAlerts } from "./alertsApi.js";
import { createCard } from "../../shared/components/card.js";
import { el, formatDate } from "../../shared/utils.js";

const TYPE_LABELS = {
  earthquake: "Earthquake",
  cyclone: "Cyclone",
  flood: "Flood",
  fire: "Fire",
  volcano: "Volcano",
  drought: "Drought",
  other: "Other",
};

const SEVERITY_LABELS = {
  red: "Critical",
  orange: "Warning",
  green: "Low risk",
};

const SOURCES = ["GDACS"];

function getContainer() {
  return document.getElementById("alerts-container");
}

export function readFilters() {
  return {
    type: document.getElementById("type-filter")?.value ?? "",
    severity: document.getElementById("severity-filter")?.value ?? "",
    country: document.getElementById("country-filter")?.value.trim() ?? "",
  };
}

function updateMeta(lastUpdate) {
  return [
    el("p", {
      class: "alerts-meta__line",
      text: `Last updated: ${formatDate(lastUpdate)}`,
    }),
    el("p", {
      class: "alerts-meta__line",
      text: `Sources consulted: ${SOURCES.join(", ")}`,
    }),
  ];
}

export function renderAlert(alert) {
  const badge = {
    type: alert.severity,
    text: SEVERITY_LABELS[alert.severity] ?? alert.severity,
  };

  const lines = [
    `${TYPE_LABELS[alert.type] ?? alert.type} · ${alert.country || "Unknown country"}`,
    formatDate(alert.date),
  ];
  if (alert.description) lines.push(alert.description);

  const card = createCard({ title: alert.title, lines, badge });

  if (alert.link) {
    card.appendChild(
      el("a", {
        class: "nexo-btn nexo-btn--secondary alerts-link",
        href: alert.link,
        target: "_blank",
        rel: "noopener",
        text: "View on GDACS",
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
    el("h2", { class: "alerts-empty__title", text: "No active alerts right now" }),
    ...updateMeta(lastUpdate)
  );
}

export function showLoading() {
  getContainer().replaceChildren(
    el("p", { class: "alerts-state", text: "Loading alerts…" })
  );
}

export function showError() {
  const retryButton = el("button", {
    class: "nexo-btn nexo-btn--secondary",
    type: "button",
    text: "Retry",
  });
  retryButton.addEventListener("click", fetchAlerts);

  getContainer().replaceChildren(
    el("h2", {
      class: "alerts-empty__title",
      text: "Could not load alerts",
    }),
    el("p", {
      class: "alerts-meta__line",
      text: "Check your internet connection or try again.",
    }),
    retryButton
  );
}

export async function fetchAlerts() {
  showLoading();
  const lastUpdate = new Date().toISOString();

  try {
    const alerts = await getAlerts(readFilters());
    if (!alerts.length) showEmptyState(lastUpdate);
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
