// Lógica del mapa de necesidades en tiempo real (módulo más votado).
// 1. INICIALIZACIÓN DEL MAPA LEAFLET
// ==========================================
// Centrado por ejemplo en Madrid [Lat, Lng], Zoom 13
const map = L.map("map").setView([40.416775, -3.70379], 13);

// Añadir capa de OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "© OpenStreetMap contributors",
}).addTo(map);

// Array para guardar las referencias a los marcadores activos
let markers = [];

let loadedNeeds = [];

// Importar las funciones de necesidadesApi.js
import { obtenerNecesidades, configurarBaseUrl } from "./necesidadesApi.js";

// El frontend (servido en un puerto, ej. 5500) y el backend (puerto 8000)
// son orígenes distintos, así que hace falta apuntar explícitamente a la API.
// TODO: mover esto a un archivo de configuración cuando haya entornos (dev/prod).
configurarBaseUrl("http://localhost:8000/api/necesidades");

// ==========================================
// 3. FUNCIONES DE RENDERIZADO Y FILTRADO
// ==========================================

/**
 * Devuelve un icono de Leaflet con color CSS basado en la prioridad.
 * Los valores de prioridad vienen del backend en español:
 * "baja" | "media" | "alta" | "critica" (ver schemas.py -> NeedPriority).
 */
function getIconByPriority(prioridad) {
  let priorityClass = "priority-low";

  if (prioridad === "alta" || prioridad === "critica") priorityClass = "priority-high";
  else if (prioridad === "media") priorityClass = "priority-medium";

  return L.divIcon({
    className: "", // Vaciamos para que no herede estilos grises/cuadrados por defecto de Leaflet
    html: `<div class="marcador-custom ${priorityClass}"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });
}

/**
 * Pinta la lista de necesidades recibida en el mapa.
 * Los campos vienen del backend en español (ver schemas.py -> NeedResponse):
 * titulo, tipo, descripcion, latitud, longitud, prioridad.
 */
function renderMap(needsList) {
  // Limpiar marcadores anteriores
  clearMarkers();

  needsList.forEach((need) => {
    const icon = getIconByPriority(need.prioridad);

    // Crear marcador con icono personalizado
    const marker = L.marker([need.latitud, need.longitud], { icon: icon });

    // Configurar el Popup del marcador
    // Maquetación usando clases de tu sistema de diseño (components.css)
    const popupContent = `
      <div class="nexo-popup">
        <div style="margin-bottom: 8px;">
          <span class="nexo-badge nexo-badge--${need.prioridad}">${need.prioridad}</span>
          <span class="nexo-badge" style="background: var(--nexo-bg-alt); border-color: var(--nexo-border);">${need.tipo}</span>
        </div>
        <h3 style="color: #000; margin: 0 0 6px 0; font-size: 1rem;">${need.titulo}</h3>
        <p style="color: #555; margin: 0; font-size: 0.85rem;">${need.descripcion}</p>
      </div>
    `;

    marker.bindPopup(popupContent);
    marker.addTo(map);

    // Guardar referencia en el array de marcadores
    markers.push(marker);
  });
}

/**
 * Elimina todos los marcadores actuales del mapa
 */
function clearMarkers() {
  markers.forEach((m) => map.removeLayer(m));
  markers = [];
}

/**
 * Filtra las necesidades según la opción seleccionada en el menú desplegable.
 * El <select id="typeFilter"> debe usar los valores reales del backend:
 * agua | alimento | medicina | refugio | herramientas | transporte.
 */
function applyFilter() {
  const selectedType = document.getElementById("typeFilter").value;

  if (selectedType === "all") {
    renderMap(loadedNeeds);
  } else {
    const filtered = loadedNeeds.filter((n) => n.tipo === selectedType);
    renderMap(filtered);
  }
}

// ==========================================
// 4. EVENTOS E INICIALIZACIÓN
// ==========================================

document.getElementById("typeFilter").addEventListener("change", applyFilter);

// Carga inicial del mapa con todos los datos desde la API.
// Se exporta para poder llamarla otra vez desde fuera (p. ej. al crear
// una necesidad nueva) y así refrescar los marcadores sin recargar la página.
export async function loadNeedsFromAPI() {
  try {
    const response = await obtenerNecesidades(); // Usar la función de necesidadesApi.js

    // Las necesidades "cubiertas" ya no aparecen en el mapa (siguen
    // viéndose en la tarjeta de la lista lateral con su marca de check).
    loadedNeeds = response.filter((need) => need.estado !== "cubierta");

    // Pintamos los marcadores en el mapa
    renderMap(loadedNeeds);
  } catch (error) {
    console.error("Error loading needs:", error);
  }
}
loadNeedsFromAPI();