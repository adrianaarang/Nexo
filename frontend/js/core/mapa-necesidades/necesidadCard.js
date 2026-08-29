// frontend/js/core/mapa-necesidades/necesidadCard.js

/**
 * Componente Objeto para las Tarjetas de Necesidad y Estados UI.
 *
 * Los campos de needData vienen del backend en español
 * (ver schemas.py -> NeedResponse): titulo (generado por el backend a
 * partir de la categoría, ya no lo escribe la persona), tipo, descripcion,
 * direccion (texto legible del lugar, ver geocodificacion.js), prioridad,
 * estado, latitud, longitud, id, creado_en, categoria_etiqueta (p. ej.
 * "💧 Agua", ya lista para pintar).
 *
 * Rediseño: el ciclo de vida ahora es un solo paso, abierta -> cubierta
 * (ver STATUS_TRANSITIONS en models.py). Ya no hay estado intermedio.
 */
const ETIQUETA_BOTON_CUBRIR = "Marcar cubierta";

export class NeedCardComponent {
  /**
   * @param {Object} needData - Datos de la necesidad
   * @param {Function} [onStatusChange] - Callback para marcar como cubierta.
   *   Recibe (id, "abierta", "cubierta") y debe devolver (o resolver a)
   *   la necesidad ya actualizada por el backend.
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
    const prioridad = (this.data.prioridad || "baja").toLowerCase();
    const tipo = (this.data.tipo || "otros").toLowerCase();
    const etiquetaCategoria = this.data.categoria_etiqueta || tipo;

    card.className = `nexo-card nexo-card--${prioridad}`;
    card.dataset.id = this.data.id;
    card.dataset.tipo = tipo;

    card.innerHTML = `
      <div class="nexo-card__header">
        <h3 class="nexo-card__title">${this.data.titulo}</h3>
        <span class="nexo-card__badge nexo-card__badge--${prioridad}">${prioridad}</span>
      </div>
      <p class="nexo-card__desc">${this.data.descripcion || "Sin descripción."}</p>
      ${this.data.direccion ? `<p class="nexo-card__address">📍 ${this.data.direccion}</p>` : ""}
      <div class="nexo-card__footer">
        <span class="nexo-card__type nexo-card__type--${tipo}">${etiquetaCategoria}</span>
        <span class="nexo-card__estado-slot"></span>
      </div>
    `;

    this.renderEstado(card);

    return card;
  }

  /**
   * Pinta la zona de estado/botón según this.data.estado actual.
   * Separado en su propio método para poder repintarlo tras un cambio
   * de estado sin reconstruir toda la tarjeta.
   */
  renderEstado(card) {
    const slot = card.querySelector(".nexo-card__estado-slot");

    if (this.data.estado === "cubierta") {
      slot.innerHTML = '<span class="check-done">✓ Cubierta</span>';
      return;
    }

    slot.innerHTML = `<button type="button" class="btn-cover" data-id="${this.data.id}">${ETIQUETA_BOTON_CUBRIR}</button>`;

    const btn = slot.querySelector(".btn-cover");
    btn.addEventListener("click", async () => {
      if (typeof this.onStatusChange !== "function") return;

      btn.disabled = true;
      btn.textContent = "Actualizando...";

      try {
        // El propio callback llama a actualizarEstadoNecesidad y nos
        // devuelve la necesidad ya actualizada por el backend.
        const necesidadActualizada = await this.onStatusChange(
          this.data.id,
          this.data.estado,
          "cubierta",
        );

        if (necesidadActualizada) {
          this.data = necesidadActualizada;
          this.renderEstado(card);
        }
      } catch (error) {
        console.error("Error cambiando el estado de la necesidad:", error);
        alert(
          `No se pudo actualizar el estado: ${error.message} ${error.detalle ? `(${error.detalle})` : ""}`,
        );
        btn.disabled = false;
        btn.textContent = ETIQUETA_BOTON_CUBRIR;
      }
    });
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
