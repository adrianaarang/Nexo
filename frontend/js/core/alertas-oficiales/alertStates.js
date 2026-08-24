// State renderers for the alerts screen (Grupo 2 - Juan). B3.
// loading / empty (D2) / error. Joel's alerts.js will call these.
import { el, formatDate } from '../../shared/utils.js';

const DEFAULT_SOURCES = ['GDACS'];

export function renderLoadingState(container) {
  container.replaceChildren(
    el('p', { class: 'nexo-card__meta', text: 'Loading alerts...' }),
  );
}

export function renderEmptyState(
  container,
  { lastUpdated = null, sources = DEFAULT_SOURCES } = {},
) {
  const card = el('div', { class: 'nexo-card' });
  card.appendChild(el('h3', { text: 'No active alerts right now' }));
  if (lastUpdated) {
    card.appendChild(
      el('p', {
        class: 'nexo-card__meta',
        text: 'Last updated: ' + formatDate(lastUpdated),
      }),
    );
  }
  card.appendChild(
    el('p', {
      class: 'nexo-card__meta',
      text: 'Sources checked: ' + sources.join(', '),
    }),
  );
  container.replaceChildren(card);
}

export function renderErrorState(
  container,
  mensaje = 'Could not load alerts. Try again in a few minutes.'
) {
  const card = el('div', { class: 'nexo-card' });
  card.appendChild(el('h3', { text: 'Something went wrong' }));
  card.appendChild(
    el('p', { class: 'nexo-card__meta', text: mensaje }),
  );
  container.replaceChildren(card);
}
