// frontend/js/core/mapa-necesidades/necesidadCard.js

/**
 * Componente Objeto para las Tarjetas de Necesidad y Estados UI.
 *
 * Los campos de needData vienen del backend en español
 * (ver schemas.py -> NeedResponse): titulo, tipo, descripcion,
 * prioridad, estado, latitud, longitud, id, creado_en.
 */
export class NeedCardComponent {
  /**
   * @param {Object} needData - Datos de la necesidad
   * @param {Function} [onStatusChange] - Callback para cambio de estado
   */
  constructor(needData, onStatusChange) {
    this.data = needData;
    this.onStatusChange = onStatusChange;
    this.element = this.createDOMElement();
  }

  /**
   * Construye el nodo DOM de la tarjeta
   */
  createDOMElement() {
    const card = document.createElement("article");

    // CAMBIO: antes era this.data.priority (inglés) -> siempre undefined,
    // por eso salía "baja" (el valor de respaldo) sin importar la prioridad real.
    const prioridad = (this.data.prioridad || "baja").toLowerCase();

    card.className = `nexo-card nexo-card--${prioridad}`;
    card.dataset.id = this.data.id;

    card.innerHTML = `
      <div class="nexo-card__header">
        <!-- CAMBIO: this.data.title -> this.data.titulo (el backend no manda "title") -->
        <h3 class="nexo-card__title">${this.data.titulo}</h3>
        <span class="nexo-card__badge nexo-card__badge--${prioridad}">${prioridad}</span>
      </div>
      <!-- CAMBIO: this.data.description -> this.data.descripcion -->
      <p class="nexo-card__desc">${this.data.descripcion || "Sin descripción."}</p>
      <div class="nexo-card__footer">
        <!-- CAMBIO: this.data.type -> this.data.tipo -->
        <span class="nexo-card__type">🏷️ ${(this.data.tipo || "General").toUpperCase()}</span>
        ${
          /* CAMBIO: this.data.status -> this.data.estado (ese es el nombre
             real del campo; "status" no existe en el contrato del backend) */
          this.data.estado !== "cubierta"
            ? `<button type="button" class="btn-cover" data-id="${this.data.id}">Marcar Cubierta</button>`
            : '<span class="check-done">✓ Cubierta</span>'
        }
      </div>
    `;

    const btnCover = card.querySelector(".btn-cover");
    if (btnCover) {
      btnCover.addEventListener("click", () => {
        if (typeof this.onStatusChange === "function") {
          // OJO (sin cambiar todavía, solo dejo la nota): el backend solo
          // permite abierta -> en_proceso -> cubierta, sin saltarse pasos
          // (ver update_need_status en models.py). Si esta necesidad está
          // "abierta", pedir "cubierta" directamente dará un 409 en cuanto
          // conectéis esto a actualizarEstadoNecesidad. Habrá que decidir
          // si el botón avanza un paso cada vez, o si mostráis dos botones.
          this.onStatusChange(this.data.id, "cubierta");
        }
      });
    }

    return card;
  }

  /**
   * Retorna el elemento DOM listo para insertar en listas o popups de Leaflet
   */
  getNode() {
    return this.element;
  }

  // Métodos Estáticos para Estados UI (Punto 22) — sin cambios
  static renderLoading() {
    const el = document.createElement("div");
    el.className = "nexo-state nexo-state--loading";
    el.innerHTML = "<p>⏳ Cargando necesidades...</p>";
    return el;
  }

  static renderEmpty() {
    const el = document.createElement("div");
    el.className = "nexo-state nexo-state--empty";
    el.innerHTML = "<p>🍃 No hay necesidades registradas.</p>";
    return el;
  }

  static renderError(msg = "Error al cargar los datos.") {
    const el = document.createElement("div");
    el.className = "nexo-state nexo-state--error";
    el.innerHTML = `<p>⚠️ ${msg}</p>`;
    return el;
  }
}