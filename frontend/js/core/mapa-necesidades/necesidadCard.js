// frontend/js/core/mapa-necesidades/necesidadCard.js

/**
 * Componente Objeto para las Tarjetas de Necesidad y Estados UI.
 *
 * Los campos de needData vienen del backend en español
 * (ver schemas.py -> NeedResponse): titulo, tipo, descripcion,
 * prioridad, estado, latitud, longitud, id, creado_en.
 *
 * El backend solo permite avanzar el estado paso a paso, sin saltos
 * ni retrocesos: abierta -> en_proceso -> cubierta (ver
 * update_need_status en models.py). SIGUIENTE_ESTADO refleja esa
 * misma regla aquí, para que el botón siempre pida el paso correcto
 * y no un 409.
 */
const SIGUIENTE_ESTADO = {
  abierta: "en_proceso",
  en_proceso: "cubierta",
};

const ETIQUETA_BOTON = {
  abierta: "Marcar en proceso",
  en_proceso: "Marcar cubierta",
};

export class NeedCardComponent {
  /**
   * @param {Object} needData - Datos de la necesidad
   * @param {Function} [onStatusChange] - Callback para cambio de estado.
   *   Recibe (id, estadoActual, siguienteEstado) y debe devolver (o
   *   resolver a) la necesidad ya actualizada por el backend.
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

    card.className = `nexo-card nexo-card--${prioridad}`;
    card.dataset.id = this.data.id;

    card.innerHTML = `
      <div class="nexo-card__header">
        <h3 class="nexo-card__title">${this.data.titulo}</h3>
        <span class="nexo-card__badge nexo-card__badge--${prioridad}">${prioridad}</span>
      </div>
      <p class="nexo-card__desc">${this.data.descripcion || "Sin descripción."}</p>
      <div class="nexo-card__footer">
        <span class="nexo-card__type">🏷️ ${(this.data.tipo || "General").toUpperCase()}</span>
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
    const siguiente = SIGUIENTE_ESTADO[this.data.estado];

    if (!siguiente) {
      // No hay siguiente paso: ya está "cubierta" (o un estado desconocido).
      slot.innerHTML = '<span class="check-done">✓ Cubierta</span>';
      return;
    }

    const etiqueta = ETIQUETA_BOTON[this.data.estado];
    slot.innerHTML = `<button type="button" class="btn-cover" data-id="${this.data.id}">${etiqueta}</button>`;

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
          siguiente,
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
        btn.textContent = etiqueta;
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