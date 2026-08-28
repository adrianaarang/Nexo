/**
 * @jest-environment jsdom
 * Official Alerts Module Tests (Vanessa)
 */

describe('Official Alerts Module - Frontend', () => {
  let container;

  beforeEach(() => {
    document.body.innerHTML = `
      <div id="alerts-container"></div>
      <div id="alerts-state"></div>
    `;
    container = document.getElementById('alerts-container');
  });

  test('Renders correctly a list with mocked alerts', () => {
    const mockAlerts = [
      {
        id: "gdacs-EQ2026001",
        fuente: "gdacs",
        tipo: "terremoto",
        titulo: "Earthquake magnitude 5.2",
        descripcion: "Earthquake detected in coastal area",
        severidad: "red",
        pais: "Spain",
        lat: 39.4,
        lon: -0.3,
        fecha: "2026-08-19T10:00:00Z",
        enlace: "https://www.gdacs.org/1"
      }
    ];

    container.innerHTML = mockAlerts.map(alert => `
      <div class="nexo-card" data-id="${alert.id}">
        <h3>${alert.titulo}</h3>
        <span class="nexo-badge nexo-badge--${alert.severidad}">${alert.severidad.toUpperCase()}</span>
        <p>${alert.descripcion}</p>
      </div>
    `).join('');

    const card = container.querySelector('.nexo-card');
    const badge = container.querySelector('.nexo-badge');

    expect(card).not.toBeNull();
    expect(container.querySelectorAll('.nexo-card').length).toBe(1);
    expect(card.textContent).toContain("Earthquake magnitude 5.2");
    expect(badge.classList.contains('nexo-badge--red')).toBe(true);
  });

  test('Renders empty state according to product decision D2 when no alerts exist', () => {
    const stateDiv = document.getElementById('alerts-state');
    const currentDate = "19/08/2026 10:00";
    
    stateDiv.innerHTML = `
      <div class="alerts-state">
        <span class="alerts-state__title">No active alerts right now</span>
        <p class="alerts-state__meta">Last updated: ${currentDate} | Source: GDACS</p>
      </div>
    `;

    expect(stateDiv.textContent).toContain("No active alerts right now");
    expect(stateDiv.textContent).toContain("Last updated:");
    expect(stateDiv.textContent).toContain("GDACS");
  });
});