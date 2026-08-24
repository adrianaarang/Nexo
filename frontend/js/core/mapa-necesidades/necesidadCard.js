// frontend/js/core/mapa-necesidades/necesidadCard.js

/**
 * Componente Objeto para las Tarjetas de Necesidad y Estados UI
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
    const priority = (this.data.priority || "baja").toLowerCase();

    card.className = `nexo-card nexo-card--${priority}`;
    card.dataset.id = this.data.id;

    card.innerHTML = `
      <div class="nexo-card__header">
        <h3 class="nexo-card__title">${this.data.title}</h3>
        <span class="nexo-card__badge nexo-card__badge--${priority}">${priority}</span>
      </div>
      <p class="nexo-card__desc">${this.data.description || "Sin descripción."}</p>
      <div class="nexo-card__footer">
        <span class="nexo-card__type">🏷️ ${(this.data.type || "General").toUpperCase()}</span>
        ${
          this.data.status !== "cubierta"
            ? `<button type="button" class="btn-cover" data-id="${this.data.id}">Marcar Cubierta</button>`
            : '<span class="check-done">✓ Cubierta</span>'
        }
      </div>
    `;

    const btnCover = card.querySelector(".btn-cover");
    if (btnCover) {
      btnCover.addEventListener("click", () => {
        if (typeof this.onStatusChange === "function") {
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

  // Métodos Estáticos para Estados UI (Punto 22)
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