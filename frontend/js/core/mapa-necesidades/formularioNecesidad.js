// frontend/js/core/mapa-necesidades/formularioNecesidad.js

/**
 * Controlador para gestionar la UI y eventos del Formulario de Necesidades
 */
export class NeedFormController {
  /**
   * @param {HTMLElement|string} container - Elemento contenedor o selector
   * @param {Function} onSubmit - Callback ejecutado al publicar una necesidad
   */
  constructor(container, onSubmit) {
    this.container =
      typeof container === "string"
        ? document.querySelector(container)
        : container;
    this.onSubmit = onSubmit;
    this.formElement = null;

    this.render();
  }

  /**
   * Genera el HTML del formulario en el DOM
   */
  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <form id="needForm" class="nexo-form">
        <h2 class="nexo-form__title">Registrar Nueva Necesidad</h2>

        <div class="nexo-form__group">
          <label for="needTitle" class="nexo-form__label">Título</label>
          <input type="text" id="needTitle" name="title" class="nexo-form__input" placeholder="Ej: Agua embotellada" required />
        </div>

        <div class="nexo-form__group">
          <label for="needDescription" class="nexo-form__label">Descripción</label>
          <textarea id="needDescription" name="description" class="nexo-form__textarea" rows="3" placeholder="Detalles de la necesidad..." required></textarea>
        </div>

        <div class="nexo-form__row">
          <div class="nexo-form__group">
            <label for="needType" class="nexo-form__label">Categoría</label>
            <select id="needType" name="type" class="nexo-form__select" required>
              <option value="alimentos">Alimentos y Agua</option>
              <option value="medicina">Medicinas</option>
              <option value="ropa">Ropa y Mantas</option>
              <option value="herramientas">Herramientas</option>
              <option value="voluntariado">Voluntariado</option>
            </select>
          </div>

          <div class="nexo-form__group">
            <label for="needPriority" class="nexo-form__label">Prioridad</label>
            <select id="needPriority" name="priority" class="nexo-form__select" required>
              <option value="baja">Baja</option>
              <option value="media" selected>Media</option>
              <option value="alta">Alta</option>
              <option value="critica">Crítica</option>
            </select>
          </div>
        </div>

        <div class="nexo-form__row">
          <div class="nexo-form__group">
            <label for="needLat" class="nexo-form__label">Latitud</label>
            <input type="number" step="any" id="needLat" name="latitude" class="nexo-form__input" readonly required />
          </div>

          <div class="nexo-form__group">
            <label for="needLng" class="nexo-form__label">Longitud</label>
            <input type="number" step="any" id="needLng" name="longitude" class="nexo-form__input" readonly required />
          </div>
        </div>

        <button type="submit" class="nexo-btn nexo-btn--primary">Publicar Necesidad</button>
      </form>
    `;

    this.formElement = this.container.querySelector("#needForm");
    this.bindEvents();
  }

  /**
   * Vincula los escuchadores de eventos
   */
  bindEvents() {
    if (!this.formElement) return;

    this.formElement.addEventListener("submit", (e) => {
      e.preventDefault();
      const formData = new FormData(this.formElement);

      const needData = {
        title: formData.get("title").trim(),
        description: formData.get("description").trim(),
        type: formData.get("type"),
        priority: formData.get("priority"),
        latitude: parseFloat(formData.get("latitude")),
        longitude: parseFloat(formData.get("longitude")),
        status: "abierta",
        createdAt: new Date().toISOString(),
      };

      if (isNaN(needData.latitude) || isNaN(needData.longitude)) {
        alert("Selecciona una ubicación en el mapa antes de publicar.");
        return;
      }

      if (typeof this.onSubmit === "function") {
        this.onSubmit(needData);
      }
    });
  }

  /**
   * Método público para actualizar las coordenadas desde el mapa
   */
  setCoordinates(lat, lng) {
    const latInput = this.formElement?.querySelector("#needLat");
    const lngInput = this.formElement?.querySelector("#needLng");

    if (latInput && lngInput) {
      latInput.value = Number(lat).toFixed(6);
      lngInput.value = Number(lng).toFixed(6);
    }
  }

  /**
   * Limpia el formulario
   */
  reset() {
    this.formElement?.reset();
  }
}
