// frontend/js/core/mapa-necesidades/necesidadCard.js

/**
 * Crea la tarjeta HTML para mostrar en la lista lateral
 * @param {Object} necesidad - Objeto con datos de la necesidad
 * @param {Function} onEstadoChange - Callback para actualizar el estado
 */
export function crearTarjetaNecesidad(necesidad, onEstadoChange) {
  const card = document.createElement("article");
  card.className = `necesidad-card prioridad-${necesidad.prioridad}`;
  card.dataset.id = necesidad.id;

  const badgeColor =
    {
      critica: "bg-red",
      alta: "bg-orange",
      media: "bg-yellow",
      baja: "bg-green",
    }[necesidad.prioridad] || "bg-gray";

  card.innerHTML = `
    <div class="card-header">
      <span class="badge ${badgeColor}">${necesidad.tipo.toUpperCase()}</span>
      <span class="prioridad-tag">${necesidad.prioridad}</span>
    </div>
    <h3 class="card-title">${necesidad.titulo}</h3>
    <p class="card-desc">${necesidad.descripcion}</p>
    <div class="card-footer">
      <span class="estado-tag estado-${necesidad.estado}">${necesidad.estado.replace("_", " ")}</span>
      ${
        necesidad.estado !== "cubierta"
          ? `<button class="btn-cubrir" data-id="${necesidad.id}">Marcar Cubierta</button>`
          : '<span class="check-done">✓ Resuelto</span>'
      }
    </div>
  `;

  // Evento para cambiar de estado
  const btnCubrir = card.querySelector(".btn-cubrir");
  if (btnCubrir) {
    btnCubrir.addEventListener("click", () => {
      onEstadoChange(necesidad.id, "cubierta");
    });
  }

  return card;
}
