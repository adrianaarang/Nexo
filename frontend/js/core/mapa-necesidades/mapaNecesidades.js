// Lógica del mapa de necesidades en tiempo real (módulo más votado).
// TODO: implementar.
// ==========================================
// 1. DATOS MOCK (Inventados hasta integrar API)
// ==========================================
const mockNeeds = [
  {
    id: 1,
    title: "Perishable food collection",
    type: "Food",
    priority: "high", // high | medium | low
    description: "Urgent need for milk cartons and canned goods.",
    latitude: 40.416775,
    longitude: -3.70379,
  },
  {
    id: 2,
    title: "Winter warm clothing",
    type: "Clothing",
    priority: "medium",
    description: "Coats and blankets for children and adults.",
    latitude: 40.42,
    longitude: -3.69,
  },
  {
    id: 3,
    title: "Volunteers for school support",
    type: "Volunteering",
    priority: "low",
    description: "Math tutoring classes two afternoons a week.",
    latitude: 40.41,
    longitude: -3.715,
  },
  {
    id: 4,
    title: "Temporary emergency shelter",
    type: "Shelter",
    priority: "high",
    description: "Space for a family affected by flooding.",
    latitude: 40.43,
    longitude: -3.7,
  },
];

let loadedNeeds = [];

// Array para guardar las referencias a los marcadores activos
let markers = [];

// ==========================================
// 2. INICIALIZACIÓN DEL MAPA LEAFLET
// ==========================================
// Centrado por ejemplo en Madrid [Lat, Lng], Zoom 13
const map = L.map("map").setView([40.416775, -3.70379], 13);

// Añadir capa de OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "© OpenStreetMap contributors",
}).addTo(map);

// ==========================================
// 3. FUNCIONES DE RENDERIZADO Y FILTRADO
// ==========================================

/**
 * Devuelve un icono de Leaflet con color CSS basado en la prioridad
 */
function getIconByPriority(priority) {
  let priorityClass = "priority-low";

  if (priority === "high") priorityClass = "priority-high";
  else if (priority === "medium") priorityClass = "priority-medium";

  return L.divIcon({
    className: "", // Vaciamos para que no herede estilos grises/cuadrados por defecto de Leaflet
    html: `<div class="marcador-custom ${priorityClass}"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });
}

/**
 * Pinta la lista de necesidades recibida en el mapa
 */
function renderMap(needsList) {
  // Limpiar marcadores anteriores
  clearMarkers();

  needsList.forEach((need) => {
    const icon = getIconByPriority(need.priority);

    // Crear marcador con icono personalizado
    const marker = L.marker([need.latitude, need.longitude], { icon: icon });

    // Configurar el Popup del marcador
    // Maquetación usando clases de tu sistema de diseño (components.css)
    const popupContent = `
      <div class="nexo-popup">
        <div style="margin-bottom: 8px;">
          <span class="nexo-badge nexo-badge--${need.priority}">${need.priority}</span>
          <span class="nexo-badge" style="background: var(--nexo-bg-alt); border-color: var(--nexo-border);">${need.type}</span>
        </div>
        <h3 style="color: #000; margin: 0 0 6px 0; font-size: 1rem;">${need.title}</h3>
        <p style="color: #555; margin: 0; font-size: 0.85rem;">${need.description}</p>
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
 * Filtra las necesidades según la opción seleccionada en el menú desplegable
 */
function applyFilter() {
  const selectedType = document.getElementById("typeFilter").value;

  if (selectedType === "all") {
    renderMap(mockNeeds);
  } else {
    const filtered = mockNeeds.filter((n) => n.type === selectedType);
    renderMap(filtered);
  }
}
/*
function applyFilter() {
  const selectedType = document.getElementById('typeFilter').value;

  if (selectedType === 'all') {
    renderMap(loadedNeeds);
  } else {
    const filtered = loadedNeeds.filter(n => n.type === selectedType);
    renderMap(filtered);
  }
}
*/

// ==========================================
// 4. EVENTOS E INICIALIZACIÓN
// ==========================================
document.getElementById("typeFilter").addEventListener("change", applyFilter);

// Carga inicial del mapa con todos los datos
/*
async function loadNeedsFromAPI() {
  try {
    const response = await fetch('https://api.your-server.com/needs');
    const data = await response.json();
    loadedNeeds = data; 

    // Pintamos los marcadores en el mapa
    renderMap(loadedNeeds);

  } catch (error) {
    console.error("Error loading needs:", error);
  }
}
loadNeedsFromAPI()
*/

renderMap(mockNeeds);
