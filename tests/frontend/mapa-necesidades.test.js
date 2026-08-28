/**
 * @jest-environment jsdom
 * Tests del módulo de Necesidades — frontend (rediseño Grupo 1).
 *
 * Sigue el mismo patrón que tests/frontend/alerts.test.js: se reproduce
 * el contrato DOM que generan necesidadCard.js / formularioNecesidad.js
 * (clases, estados, atributos) en vez de importar los módulos ES
 * directamente, ya que el proyecto todavía no tiene un runner de Jest
 * con soporte ESM configurado (ver package.json).
 */

describe('Necesidades Module - Tarjetas', () => {
  let container;

  beforeEach(() => {
    document.body.innerHTML = `<div id="contenedor-tarjetas"></div>`;
    container = document.getElementById('contenedor-tarjetas');
  });

  function renderCard(need) {
    const prioridad = (need.prioridad || 'baja').toLowerCase();
    const tipo = (need.tipo || 'otros').toLowerCase();
    const etiqueta = need.categoria_etiqueta || tipo;

    const estadoHtml =
      need.estado === 'cubierta'
        ? '<span class="check-done">✓ Cubierta</span>'
        : `<button type="button" class="btn-cover" data-id="${need.id}">Marcar cubierta</button>`;

    const direccionHtml = need.direccion
      ? `<p class="nexo-card__address">📍 ${need.direccion}</p>`
      : '';

    container.innerHTML += `
      <article class="nexo-card nexo-card--${prioridad}" data-id="${need.id}" data-tipo="${tipo}">
        <div class="nexo-card__header">
          <h3 class="nexo-card__title">${need.titulo}</h3>
          <span class="nexo-card__badge nexo-card__badge--${prioridad}">${prioridad}</span>
        </div>
        <p class="nexo-card__desc">${need.descripcion || 'Sin descripción.'}</p>
        ${direccionHtml}
        <div class="nexo-card__footer">
          <span class="nexo-card__type">${etiqueta}</span>
          <span class="nexo-card__estado-slot">${estadoHtml}</span>
        </div>
      </article>
    `;
  }

  test('Renders a card with the emoji category label and priority badge', () => {
    renderCard({
      id: 1,
      titulo: 'Necesidad de agua',
      tipo: 'agua',
      categoria_etiqueta: '💧 Agua',
      descripcion: 'Punto sin agua potable desde hace dos días',
      direccion: 'Puerta del Sol, Madrid',
      prioridad: 'alta',
      estado: 'abierta',
    });

    const card = container.querySelector('.nexo-card');

    expect(card).not.toBeNull();
    expect(card.dataset.tipo).toBe('agua');
    expect(card.classList.contains('nexo-card--alta')).toBe(true);
    expect(card.textContent).toContain('💧 Agua');
    // El título ya no lo escribe la persona (se quitó del formulario):
    // lo genera el backend a partir de la categoría.
    expect(card.textContent).toContain('Necesidad de agua');
  });

  test('Renders the geocoded address when present', () => {
    renderCard({
      id: 4,
      titulo: 'Necesidad de refugio',
      tipo: 'refugio',
      categoria_etiqueta: '🏠 Refugio',
      direccion: 'Plaza Mayor, Madrid',
      prioridad: 'media',
      estado: 'abierta',
    });

    const direccion = container.querySelector('.nexo-card__address');

    expect(direccion).not.toBeNull();
    expect(direccion.textContent).toContain('Plaza Mayor, Madrid');
  });

  test('Renders no address line when the need has no address', () => {
    renderCard({
      id: 5,
      titulo: 'Necesidad de otros',
      tipo: 'otros',
      categoria_etiqueta: '📦 Otros',
      direccion: '',
      prioridad: 'baja',
      estado: 'abierta',
    });

    expect(container.querySelector('.nexo-card__address')).toBeNull();
  });

  test('An open need shows the "Marcar cubierta" button (single-step lifecycle)', () => {
    renderCard({
      id: 2,
      titulo: 'Alojamiento temporal',
      tipo: 'refugio',
      categoria_etiqueta: '🏠 Refugio',
      prioridad: 'alta',
      estado: 'abierta',
    });

    const boton = container.querySelector('.btn-cover');

    expect(boton).not.toBeNull();
    expect(boton.textContent).toBe('Marcar cubierta');
    // Ya no existe un estado intermedio "en_proceso": el único botón posible
    // es el que avanza directamente a "cubierta".
    expect(container.innerHTML).not.toContain('en_proceso');
    expect(container.innerHTML).not.toContain('en proceso');
  });

  test('A covered need shows the check mark instead of a button', () => {
    renderCard({
      id: 3,
      titulo: 'Comida para 30 personas',
      tipo: 'alimentos',
      categoria_etiqueta: '🍞 Alimentos',
      prioridad: 'media',
      estado: 'cubierta',
    });

    expect(container.querySelector('.btn-cover')).toBeNull();
    expect(container.querySelector('.check-done')).not.toBeNull();
    expect(container.textContent).toContain('✓ Cubierta');
  });

  test('Renders empty state according to the loading/empty/error contract', () => {
    container.innerHTML = '<p>🍃 No hay necesidades registradas.</p>';

    expect(container.textContent).toContain('No hay necesidades registradas');
  });
});

describe('Necesidades Module - Formulario simplificado (categorías cerradas)', () => {
  let categorias;

  // Reproduce la lógica de selección de setupCategorias() en
  // formularioNecesidad.js: un solo botón activo a la vez, marcado con
  // la clase is-selected y aria-pressed="true".
  function bindCategoryButtons(root) {
    const botones = root.querySelectorAll('.nexo-categoria-btn');
    let seleccionado = null;

    botones.forEach((boton) => {
      boton.setAttribute('aria-pressed', 'false');
      boton.addEventListener('click', () => {
        botones.forEach((b) => {
          b.classList.remove('is-selected');
          b.setAttribute('aria-pressed', 'false');
        });
        boton.classList.add('is-selected');
        boton.setAttribute('aria-pressed', 'true');
        seleccionado = boton.dataset.tipo;
      });
    });

    return { getSeleccionado: () => seleccionado };
  }

  beforeEach(() => {
    document.body.innerHTML = `
      <div class="nexo-categorias">
        <button type="button" class="nexo-categoria-btn" data-tipo="agua">💧 Agua</button>
        <button type="button" class="nexo-categoria-btn" data-tipo="alimentos">🍞 Alimentos</button>
        <button type="button" class="nexo-categoria-btn" data-tipo="parafarmacia">💊 Parafarmacia</button>
        <button type="button" class="nexo-categoria-btn" data-tipo="ropa">👕 Ropa</button>
        <button type="button" class="nexo-categoria-btn" data-tipo="higiene">🧴 Higiene</button>
        <button type="button" class="nexo-categoria-btn" data-tipo="refugio">🏠 Refugio</button>
        <button type="button" class="nexo-categoria-btn" data-tipo="transporte">🚗 Transporte</button>
        <button type="button" class="nexo-categoria-btn" data-tipo="otros">📦 Otros</button>
      </div>
    `;
    categorias = document.querySelector('.nexo-categorias');
  });

  test('Exposes exactly the 8 closed categories agreed with the backend', () => {
    const tipos = Array.from(
      categorias.querySelectorAll('.nexo-categoria-btn'),
    ).map((b) => b.dataset.tipo);

    expect(tipos).toEqual([
      'agua',
      'alimentos',
      'parafarmacia',
      'ropa',
      'higiene',
      'refugio',
      'transporte',
      'otros',
    ]);
  });

  test('Clicking a category button selects it exclusively', () => {
    const controller = bindCategoryButtons(categorias);
    const botones = categorias.querySelectorAll('.nexo-categoria-btn');

    botones[0].click(); // agua
    expect(controller.getSeleccionado()).toBe('agua');
    expect(botones[0].classList.contains('is-selected')).toBe(true);

    botones[3].click(); // ropa
    expect(controller.getSeleccionado()).toBe('ropa');
    expect(botones[3].classList.contains('is-selected')).toBe(true);
    // Solo puede haber una categoría seleccionada a la vez.
    expect(botones[0].classList.contains('is-selected')).toBe(false);
    expect(
      categorias.querySelectorAll('.is-selected').length,
    ).toBe(1);
  });
});

describe('Necesidades Module - Dirección y coordenadas confirmadas', () => {
  // Reproduce la lógica de setupDireccion()/confirmarUbicacion() de
  // formularioNecesidad.js: las coordenadas de GPS/clic en el mapa quedan
  // "confirmadas" (no hay que geocodificar de nuevo al enviar) mientras la
  // persona no edite el campo de dirección a mano.
  function crearControladorDireccion(input) {
    let coordenadasConfirmadas = null;

    input.addEventListener('input', () => {
      coordenadasConfirmadas = null;
    });

    return {
      confirmarUbicacion(lat, lng, direccionLegible) {
        coordenadasConfirmadas = { lat, lng };
        input.value = direccionLegible; // asignación programática: no dispara 'input'
      },
      getCoordenadasConfirmadas: () => coordenadasConfirmadas,
    };
  }

  let input;

  beforeEach(() => {
    document.body.innerHTML = `<input type="text" id="input-direccion" />`;
    input = document.getElementById('input-direccion');
  });

  test('Filling the address via GPS/map click keeps the coordinates confirmed', () => {
    const controller = crearControladorDireccion(input);

    controller.confirmarUbicacion(40.4168, -3.7038, 'Puerta del Sol, Madrid');

    expect(input.value).toBe('Puerta del Sol, Madrid');
    expect(controller.getCoordenadasConfirmadas()).toEqual({
      lat: 40.4168,
      lng: -3.7038,
    });
  });

  test('Manually typing in the address field invalidates the confirmed coordinates', () => {
    const controller = crearControladorDireccion(input);
    controller.confirmarUbicacion(40.4168, -3.7038, 'Puerta del Sol, Madrid');

    // Simula tecleo real de la persona (dispatchEvent sí lanza 'input',
    // a diferencia de asignar .value directamente).
    input.value = 'Calle Mayor 3, Madrid';
    input.dispatchEvent(new Event('input'));

    expect(controller.getCoordenadasConfirmadas()).toBeNull();
  });
});
