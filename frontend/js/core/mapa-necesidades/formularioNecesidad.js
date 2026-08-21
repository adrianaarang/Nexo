// frontend/js/core/mapa-necesidades/formularioNecesidad.js

/**
 * Módulo para gestionar la creación y comportamiento del formulario de necesidades
 */

/**
 * Renderiza e inicializa el formulario de registro de necesidad en un contenedor dado.
 * @param {HTMLElement} container - Contenedor DOM donde se insertará el formulario.
 * @param {Function} onSubmit - Callback ejecutado al enviar el formulario con datos válidos.
 */
export function initNeedForm(container, onSubmit) {
  if (!container) return;

  container.innerHTML = `
    <form id="needForm" class="nexo-form">
      <h2 class="nexo-form__title">Registrar Nueva Necesidad</h2>

      <div class="nexo-form__group">
        <label for="needTitle" class="nexo-form__label">Título</label>
        <input 
          type="text" 
          id="needTitle" 
          name="title" 
          class="nexo-form__input" 
          placeholder="Ej: Agua embotellada o mantas" 
          required 
        />
      </div>

      <div class="nexo-form__group">
        <label for="needDescription" class="nexo-form__label">Descripción</label>
        <textarea 
          id="needDescription" 
          name="description" 
          class="nexo-form__textarea" 
          rows="3" 
          placeholder="Describe la situación y detalles específicos..." 
          required
        ></textarea>
      </div>

      <div class="nexo-form__row">
        <div class="nexo-form__group">
          <label for="needType" class="nexo-form__label">Categoría / Tipo</label>
          <select id="needType" name="type" class="nexo-form__select" required>
            <option value="alimentos">Alimentos y Agua</option>
            <option value="medicina">Medicinas / Primeros Auxilios</option>
            <option value="ropa">Ropa y Mantas</option>
            <option value="herramientas">Herramientas / Maquinaria</option>
            <option value="voluntariado">Manos de Obra / Voluntariado</option>
            <option value="otro">Otro</option>
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

      <!-- Coordenadas capturadas desde el mapa o geolocalización -->
      <div class="nexo-form__row">
        <div class="nexo-form__group">
          <label for="needLat" class="nexo-form__label">Latitud</label>
          <input 
            type="number" 
            step="any" 
            id="needLat" 
            name="latitude" 
            class="nexo-form__input" 
            placeholder="36.465" 
            readonly 
            required 
          />
        </div>

        <div class="nexo-form__group">
          <label for="needLng" class="nexo-form__label">Longitud</label>
          <input 
            type="number" 
            step="any" 
            id="needLng" 
            name="longitude" 
            class="nexo-form__input" 
            placeholder="-6.198" 
            readonly 
            required 
          />
        </div>
      </div>

      <p class="nexo-form__hint">💡 Haz clic en el mapa para fijar la ubicación exacta.</p>

      <button type="submit" class="nexo-btn nexo-btn--primary">
        Publicar Necesidad
      </button>
    </form>
  `;

  const formElement = container.querySelector("#needForm");
  
  formElement.addEventListener("submit", (event) => {
    event.preventDefault();
    handleFormSubmit(formElement, onSubmit);
  });
}

/**
 * Procesa el envío del formulario, extrae los datos y ejecuta el callback.
 * @param {HTMLFormElement} formElement - Elemento del formulario.
 * @param {Function} onSubmit - Callback callback con el payload procesado.
 */
function handleFormSubmit(formElement, onSubmit) {
  const formData = new FormData(formElement);

  const needData = {
    title: formData.get("title").trim(),
    description: formData.get("description").trim(),
    type: formData.get("type"),
    priority: formData.get("priority"),
    latitude: parseFloat(formData.get("latitude")),
    longitude: parseFloat(formData.get("longitude")),
    status: "abierta", // Estado por defecto al crear
    createdAt: new Date().toISOString()
  };

  if (isNaN(needData.latitude) || isNaN(needData.longitude)) {
    alert("Por favor, selecciona una ubicación en el mapa antes de publicar.");
    return;
  }

  onSubmit(needData);
}

/**
 * Actualiza los campos de coordenadas del formulario al hacer clic en el mapa.
 * @param {number} latitude - Valor de la latitud.
 * @param {number} longitude - Valor de la longitud.
 */
export function setFormCoordinates(latitude, longitude) {
  const latInput = document.getElementById("needLat");
  const lngInput = document.getElementById("needLng");

  if (latInput && lngInput) {
    latInput.value = latitude.toFixed(6);
    lngInput.value = longitude.toFixed(6);
  }
}

/**
 * Limpia y reinicia los campos del formulario tras un envío exitoso.
 */
export function clearNeedForm() {
  const formElement = document.getElementById("needForm");
  if (formElement) {
    formElement.reset();
  }
}