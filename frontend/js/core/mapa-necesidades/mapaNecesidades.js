// Lógica del mapa de necesidades en tiempo real (módulo más votado).
// TODO: implementar.
// ==========================================
// 1. DATOS MOCK (Inventados hasta integrar API)
// ==========================================
const necesidadesMock = [
  {
    id: 1,
    titulo: "Recogida de alimentos perecederos",
    tipo: "Alimentos",
    prioridad: "alta", // alta | media | baja
    descripcion: "Se necesitan cajas de leche y conservas urgentes.",
    latitud: 40.416775,
    longitud: -3.703790
  },
  {
    id: 2,
    titulo: "Ropa de abrigo para invierno",
    tipo: "Ropa",
    prioridad: "media",
    descripcion: "Abrigos y mantas para niños y adultos.",
    latitud: 40.420000,
    longitud: -3.690000
  },
  {
    id: 3,
    titulo: "Voluntarios para apoyo escolar",
    tipo: "Voluntariado",
    prioridad: "baja",
    descripcion: "Clases de refuerzo en matemáticas dos tardes a la semana.",
    latitud: 40.410000,
    longitud: -3.715000
  },
  {
    id: 4,
    titulo: "Alojamiento temporal de emergencia",
    tipo: "Alojamiento",
    prioridad: "alta",
    descripcion: "Espacio para una familia afectada por inundaciones.",
    latitud: 40.430000,
    longitud: -3.700000
  }
];

let necesidadesCargadas = [];

// Array para guardar las referencias a los marcadores activos
let marcadores = [];

// ==========================================
// 2. INICIALIZACIÓN DEL MAPA LEAFLET
// ==========================================
// Centrado por ejemplo en Madrid [Lat, Lng], Zoom 13
const mapa = L.map('mapa').setView([40.416775, -3.703790], 13);

// Añadir capa de OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap contributors'
}).addTo(mapa);

// ==========================================
// 3. FUNCIONES DE RENDERIZADO Y FILTRADO
// ==========================================

/**
 * Devuelve un icono de Leaflet con color CSS basado en la prioridad
 */
function obtenerIconoPorPrioridad(prioridad) {
  let clasePrioridad = 'prioridad-baja';

  if (prioridad === 'alta') clasePrioridad = 'prioridad-alta';
  else if (prioridad === 'media') clasePrioridad = 'prioridad-media';

  return L.divIcon({
    className: '', // Vaciamos para que no herede estilos grises/cuadrados por defecto de Leaflet
    html: `<div class="marcador-custom ${clasePrioridad}"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9]
  });
}

/**
 * Pinta la lista de necesidades recibida en el mapa
 */
function pintarMapa(listaNecesidades) {
  // Limpiar marcadores anteriores
  limpiarMarcadores();

  listaNecesidades.forEach((necesidad) => {
    const icono = obtenerIconoPorPrioridad(necesidad.prioridad);

    // Crear marcador con icono personalizado
    const marcador = L.marker([necesidad.latitud, necesidad.longitud], { icon: icono });

    // Configurar el Popup del marcador
    // Maquetación usando clases de tu sistema de diseño (components.css)
    const contenidoPopup = `
      <div class="nexo-popup">
        <div style="margin-bottom: 8px;">
          <span class="nexo-badge nexo-badge--${necesidad.prioridad}">${necesidad.prioridad}</span>
          <span class="nexo-badge" style="background: var(--nexo-bg-alt); border-color: var(--nexo-border);">${necesidad.tipo}</span>
        </div>
        <h3 style="color: #000; margin: 0 0 6px 0; font-size: 1rem;">${necesidad.titulo}</h3>
        <p style="color: #555; margin: 0; font-size: 0.85rem;">${necesidad.descripcion}</p>
      </div>
    `;

    marcador.bindPopup(contenidoPopup);
    marcador.addTo(mapa);

    // Guardar referencia en el array de marcadores
    marcadores.push(marcador);
  });
}

/**
 * Elimina todos los marcadores actuales del mapa
 */
function limpiarMarcadores() {
  marcadores.forEach(m => mapa.removeLayer(m));
  marcadores = [];
}

/**
 * Filtra las necesidades según la opción seleccionada en el menú desplegable
 */
function aplicarFiltro() {
  const tipoSeleccionado = document.getElementById('filtroTipo').value;

  if (tipoSeleccionado === 'todos') {
    pintarMapa(necesidadesMock);
  } else {
    const filtradas = necesidadesMock.filter(n => n.tipo === tipoSeleccionado);
    pintarMapa(filtradas);
  }
}
/*
function aplicarFiltro() {
  const tipoSeleccionado = document.getElementById('filtroTipo').value;

  if (tipoSeleccionado === 'todos') {
    pintarMapa(necesidadesCargadas);
  } else {
    const filtradas = necesidadesCargadas.filter(n => n.tipo === tipoSeleccionado);
    pintarMapa(filtradas);
  }
}
*/


// ==========================================
// 4. EVENTOS E INICIALIZACIÓN
// ==========================================
document.getElementById('filtroTipo').addEventListener('change', aplicarFiltro);

// Carga inicial del mapa con todos los datos
/*
async function cargarNecesidadesDesdeAPI() {
  try {
    const response = await fetch('https://api.tu-servidor.com/necesidades');
    const datos = await response.json();
    necesidadesCargadas = datos; 

    // Pintamos los marcadores en el mapa
    pintarMapa(necesidadesCargadas);

  } catch (error) {
    console.error("Error al cargar necesidades:", error);
  }
}
cargarNecesidadesDesdeAPI()
*/


pintarMapa(necesidadesMock);