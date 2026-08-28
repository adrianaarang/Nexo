// Donations list and form — Team 3 frontend.
// Lista y formulario de donaciones — Equipo 3 frontend.
import { getDonations, markDonationAsDelivered, postDonation } from "./donacionesApi.js";

const list           = document.getElementById("lista-donaciones");
const statusEl       = document.getElementById("estado-lista");
const form           = document.getElementById("form-donacion");
const filterType     = document.getElementById("filtro-tipo");
const filterOrder    = document.getElementById("filtro-orden");
const filterCategory = document.getElementById("filtro-categoria");

function initDropdowns() {
  document.querySelectorAll(".nexo-select").forEach(sel => {
    const trigger = sel.querySelector(".nexo-select__trigger");
    const menu    = sel.querySelector(".nexo-select__menu");
    const label   = sel.querySelector(".nexo-select__label");

    trigger.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = sel.classList.contains("nexo-select--abierto");
      document.querySelectorAll(".nexo-select.nexo-select--abierto").forEach(s => s.classList.remove("nexo-select--abierto"));
      if (!isOpen) sel.classList.add("nexo-select--abierto");
    });

    // Form dropdowns don't reload the list on selection.
    // Los dropdowns del formulario no recargan la lista al seleccionar.
    const isFormDropdown = form.contains(sel);

    menu.querySelectorAll("li").forEach(li => {
      li.addEventListener("click", () => {
        sel.dataset.value = li.dataset.value;
        label.textContent = li.textContent;
        label.classList.remove("nexo-select__label--placeholder");
        menu.querySelectorAll("li").forEach(l => l.classList.remove("nexo-select__opcion--activa"));
        li.classList.add("nexo-select__opcion--activa");
        sel.classList.remove("nexo-select--abierto");
        if (!isFormDropdown) loadDonations();
      });
    });
  });

  document.addEventListener("click", () => {
    document.querySelectorAll(".nexo-select.nexo-select--abierto").forEach(s => s.classList.remove("nexo-select--abierto"));
  });
}

// SVG icons keyed by exact category name (must match backend values).
// Íconos SVG indexados por nombre exacto de categoría (debe coincidir con el backend).
const ICONS = {
  "Agua": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 2C12 2 5 9.5 5 14a7 7 0 0 0 14 0C19 9.5 12 2 12 2z"/>
  </svg>`,
  "Comida": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="7" width="18" height="13" rx="2"/>
    <path d="M3 11h18"/>
    <path d="M8 7V4"/>
    <path d="M16 7V4"/>
  </svg>`,
  "Mantas": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="5" width="18" height="14" rx="2"/>
    <path d="M3 9h18"/>
    <path d="M7 5v4"/>
    <path d="M12 5v4"/>
    <path d="M17 5v4"/>
  </svg>`,
  "Ropa infantil": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 6l4-2 5 3 5-3 4 2-2 5h-3v9H8V11H5z"/>
    <circle cx="12" cy="18" r="1.5"/>
  </svg>`,
  "Ropa de adultos": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 6l4-2 5 3 5-3 4 2-2 5h-3v9H8V11H5z"/>
  </svg>`,
  "Productos de higiene": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M7 2h10v4H7z"/>
    <rect x="5" y="6" width="14" height="15" rx="2"/>
    <path d="M9 11h6"/>
    <path d="M9 15h4"/>
  </svg>`,
  "Alojamiento temporal": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 17l4-8 5 5 3-3 6 6"/>
    <path d="M3 17h18"/>
    <path d="M9 17v-4"/>
  </svg>`,
  "Combustible y/o baterías": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="6" y="2" width="12" height="18" rx="2"/>
    <path d="M10 2v2h4V2"/>
    <path d="M12 8v4"/>
    <path d="M10 10h4"/>
  </svg>`,
  "Servicios de comunicación": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M5 12.5a9.5 9.5 0 0 1 14 0"/>
    <path d="M8.5 16a5.5 5.5 0 0 1 7 0"/>
    <circle cx="12" cy="19.5" r="1"/>
  </svg>`,
  "Medicamentos": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="4" y="3" width="16" height="18" rx="2"/>
    <path d="M9 9h6"/>
    <path d="M9 13h6"/>
    <path d="M9 17h4"/>
    <path d="M8 3v3h8V3"/>
  </svg>`,
  "Material de primeros auxilios": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2"/>
    <path d="M12 8v8"/>
    <path d="M8 12h8"/>
  </svg>`,
  "Artículos para bebés": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M9 3h6l1 5H8z"/>
    <path d="M8 8c0 5-2 8-2 11h12c0-3-2-6-2-11"/>
    <path d="M10 14h4"/>
  </svg>`,
  "Herramientas": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3-3a6 6 0 0 1-8.1 8.1L6 21a2 2 0 0 1-3-3l6.7-6.1a6 6 0 0 1 8.1-8.1l-3.1 3z"/>
  </svg>`,
  "Transporte": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="1" y="8" width="22" height="10" rx="2"/>
    <path d="M5 8V5a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"/>
    <circle cx="7" cy="18" r="2"/>
    <circle cx="17" cy="18" r="2"/>
  </svg>`,
};

function getIcon(resource) {
  return ICONS[resource] || `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 8H3l1.5 11h15z"/>
    <path d="M3 8l2-4h14l2 4"/>
    <path d="M12 8v11"/>
  </svg>`;
}

function renderCard(d) {
  const status   = d.estado ?? "activa";
  const isActive = status === "activa";
  return `
    <div class="donacion-card" id="donacion-${d.id}">
      <div class="donacion-led donacion-led--${status}">
        <span class="donacion-led__punto"></span>
        ${isActive ? "Activa" : "Entregada"}
      </div>
      <div class="donacion-card__icono">${getIcon(d.recurso)}</div>
      <div class="donacion-card__contenido">
        <h3>${d.recurso}</h3>
        ${d.descripcion ? `<p class="donacion-card__desc">${d.descripcion}</p>` : ""}
        ${d.cantidad    ? `<p>Cantidad: ${d.cantidad}</p>` : ""}
        <p>Contacto: ${d.contacto}</p>
        ${isActive ? `<button class="donacion-card__btn" data-id="${d.id}">Marcar como entregada</button>` : ""}
      </div>
    </div>
  `;
}

// Event delegation — avoids inline onclick which doesn't work in ES modules.
// Delegación de eventos — el onclick inline no funciona en módulos ES.
list.addEventListener("click", async (e) => {
  const btn = e.target.closest(".donacion-card__btn");
  if (btn) await markAsDelivered(Number(btn.dataset.id));
});

async function markAsDelivered(id) {
  try {
    await markDonationAsDelivered(id);
    await loadDonations();
    return;
  } catch {
    showStatus("No se pudo actualizar el estado de la donación.");
    // Backend unavailable — visual update only. / Sin backend, solo actualización visual.
  }

}

function showStatus(text) {
  statusEl.textContent = text;
  statusEl.hidden = false;
}

function hideStatus() {
  statusEl.hidden = true;
}

async function loadDonations() {
  const type     = filterType.dataset.value     || null;
  const order    = filterOrder.dataset.value    || "recientes";
  const category = filterCategory.dataset.value || null;

  list.innerHTML = "";
  showStatus("Cargando...");

  let data;
  try {
    data = await getDonations(type);
  } catch {
    showStatus("No se pudieron cargar las donaciones. Inténtalo de nuevo más tarde.");
    return;
  }

  if (category) data = data.filter(d => d.recurso === category);

  data.sort((a, b) => {
    const ta = new Date(a.creado_en).getTime();
    const tb = new Date(b.creado_en).getTime();
    return order === "antiguos" ? ta - tb : tb - ta;
  });

  hideStatus();

  if (data.length === 0) {
    showStatus("No hay donaciones para los filtros seleccionados.");
    return;
  }

  list.innerHTML = data.map(renderCard).join("");

}

function resetFormDropdowns() {
  const typeEl = document.getElementById("tipo");
  typeEl.dataset.value = "ofrecida";
  typeEl.querySelector(".nexo-select__label").textContent = "Ofrezco recursos";
  typeEl.querySelectorAll("li").forEach((li, i) => li.classList.toggle("nexo-select__opcion--activa", i === 0));

  const resourceEl    = document.getElementById("recurso");
  resourceEl.dataset.value = "";
  const resourceLabel = resourceEl.querySelector(".nexo-select__label");
  resourceLabel.textContent  = "Selecciona una categoría";
  resourceLabel.classList.add("nexo-select__label--placeholder");
  resourceEl.querySelectorAll("li").forEach(li => li.classList.remove("nexo-select__opcion--activa"));
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const resourceEl = document.getElementById("recurso");
  if (!resourceEl.dataset.value) {
    const trigger = resourceEl.querySelector(".nexo-select__trigger");
    trigger.classList.add("nexo-select__trigger--error");
    setTimeout(() => trigger.classList.remove("nexo-select__trigger--error"), 1500);
    return;
  }

  const btn = form.querySelector("button[type=submit]");
  btn.disabled    = true;
  btn.textContent = "Publicando...";

  // API field names (tipo, recurso, etc.) are part of the backend contract — kept as-is.
  // Los nombres de campo de la API son parte del contrato con el backend — no se traducen.
  const payload = {
    tipo:       document.getElementById("tipo").dataset.value,
    recurso:    resourceEl.dataset.value,
    cantidad:   form.querySelector("#cantidad").value,
    descripcion: form.querySelector("#descripcion").value,
    contacto:   form.querySelector("#contacto").value,
  };

  try {
    await postDonation(payload);
    form.reset();
    resetFormDropdowns();
    document.getElementById("contador-desc").textContent = "0 / 1000";
    await loadDonations();
  } catch {
    alert("No se pudo publicar. Verifica tu conexión.");
  } finally {
    btn.disabled    = false;
    btn.textContent = "Publicar";
  }
});

const descriptionEl = form.querySelector("#descripcion");
const counterEl     = document.getElementById("contador-desc");
descriptionEl.addEventListener("input", () => {
  counterEl.textContent = `${descriptionEl.value.length} / 1000`;
});

initDropdowns();
loadDonations();
