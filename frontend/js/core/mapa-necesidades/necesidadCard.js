/**
 * Crea la tarjeta HTML para mostrar en la lista lateral utilizando BEM-lite (nexo-card)
 * @param {Object} need - Objeto con datos de la necesidad
 * @param {Function} onStatusChange - Callback para actualizar el estado
 * @returns {HTMLElement} Elemento DOM de la tarjeta
 */
export function createNeedCard(need, onStatusChange) {
  const card = document.createElement("article");
  const priority = (need.priority || "baja").toLowerCase();

  card.className = `nexo-card nexo-card--${priority}`;
  card.dataset.id = need.id;

  const typeText = (need.type || "General").toUpperCase();
  const statusText = (need.status || "abierta").replace("_", " ");

  card.innerHTML = `
    <div class="nexo-card__header">
      <h3 class="nexo-card__title">${need.title}</h3>
      <span class="nexo-card__badge nexo-card__badge--${priority}">
        ${priority}
      </span>
    </div>
    <p class="nexo-card__desc">${need.description || "Sin descripción proporcionada."}</p>
    <div class="nexo-card__footer">
      <span class="nexo-card__type">🏷️ ${typeText}</span>
      <span class="nexo-card__status nexo-card__status--${need.status}">
        ${statusText}
      </span>
      ${
        need.status !== "cubierta"
          ? `<button type="button" class="btn-cover" data-id="${need.id}">Marcar Cubierta</button>`
          : '<span class="check-done">✓ Cubierta</span>'
      }
    </div>
  `;

  // Evento para cambiar de estado al pulsar el botón
  const btnCover = card.querySelector(".btn-cover");
  if (btnCover) {
    btnCover.addEventListener("click", () => {
      onStatusChange(need.id, "cubierta");
    });
  }

  return card;
}

/**
 * Renderiza el estado de vacío cuando no hay necesidades (Cumple Punto 22)
 * @returns {HTMLElement} Elemento DOM
 */
export function renderEmptyState() {
  const container = document.createElement("div");
  container.className = "nexo-state nexo-state--empty";
  container.innerHTML = `
    <p>🍃 No hay necesidades registradas en esta zona actualmente.</p>
  `;
  return container;
}

/**
 * Renderiza el estado de carga (Loading skeleton/spinner)
 * @returns {HTMLElement} Elemento DOM
 */
export function renderLoadingState() {
  const container = document.createElement("div");
  container.className = "nexo-state nexo-state--loading";
  container.innerHTML = `
    <p>⏳ Cargando necesidades en tiempo real...</p>
  `;
  return container;
}

/**
 * Renderiza el estado de error cuando la API o conexión falla
 * @param {string} message - Mensaje explicativo del error
 * @returns {HTMLElement} Elemento DOM
 */
export function renderErrorState(
  message = "Error al conectar con la red de necesidades.",
) {
  const container = document.createElement("div");
  container.className = "nexo-state nexo-state--error";
  container.innerHTML = `
    <p>⚠️ ${message}</p>
  `;
  return container;
}
