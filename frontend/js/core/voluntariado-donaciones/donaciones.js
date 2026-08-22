// Alta y listado de donaciones — Equipo 3 (frontend).
import { getDonaciones, postDonacion } from "./donacionesApi.js";

const MOCK = [
  { id: 1, tipo: "ofrecida", recurso: "Agua embotellada", cantidad: "50 litros", contacto: "voluntario@ejemplo.com", creado_en: "2026-08-21T10:00:00Z" },
  { id: 2, tipo: "solicitada", recurso: "Mantas", cantidad: "10 unidades", contacto: "afectado@ejemplo.com", creado_en: "2026-08-21T11:00:00Z" },
  { id: 3, tipo: "ofrecida", recurso: "Ropa de abrigo infantil", cantidad: "", contacto: "cruz.roja@ejemplo.com", creado_en: "2026-08-21T12:00:00Z" },
];

const lista = document.getElementById("lista-donaciones");
const estadoEl = document.getElementById("estado-lista");
const form = document.getElementById("form-donacion");
const filtro = document.getElementById("filtro-tipo");

function renderTarjeta(d) {
  const esOfrecida = d.tipo === "ofrecida";
  return `
    <div class="nexo-card">
      <span class="nexo-card__num">#${d.id}</span>
      <span class="nexo-badge ${esOfrecida ? "nexo-badge--green" : "nexo-badge--orange"}">
        ${esOfrecida ? "Ofrecida" : "Solicitada"}
      </span>
      <h3>${d.recurso}</h3>
      ${d.cantidad ? `<p class="nexo-card__meta">Cantidad: ${d.cantidad}</p>` : ""}
      <p class="nexo-card__meta">Contacto: ${d.contacto}</p>
    </div>
  `;
}

function mostrarEstado(texto) {
  estadoEl.textContent = texto;
  estadoEl.hidden = false;
}

function ocultarEstado() {
  estadoEl.hidden = true;
}

async function cargarDonaciones(tipo = null) {
  lista.innerHTML = "";
  mostrarEstado("Cargando...");

  let datos;
  try {
    datos = await getDonaciones(tipo);
  } catch {
    datos = tipo ? MOCK.filter(d => d.tipo === tipo) : MOCK;
  }

  ocultarEstado();

  if (datos.length === 0) {
    mostrarEstado("No hay donaciones en este momento.");
    return;
  }

  lista.innerHTML = datos.map(renderTarjeta).join("");
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = form.querySelector("button[type=submit]");
  btn.disabled = true;
  btn.textContent = "Publicando...";

  const datos = {
    tipo: form.querySelector("#tipo").value,
    recurso: form.querySelector("#recurso").value,
    cantidad: form.querySelector("#cantidad").value,
    contacto: form.querySelector("#contacto").value,
  };

  try {
    await postDonacion(datos);
    form.reset();
    await cargarDonaciones(filtro.value || null);
  } catch {
    alert("No se pudo publicar. Verifica tu conexión.");
  } finally {
    btn.disabled = false;
    btn.textContent = "Publicar";
  }
});

filtro.addEventListener("change", () => {
  cargarDonaciones(filtro.value || null);
});

cargarDonaciones();
