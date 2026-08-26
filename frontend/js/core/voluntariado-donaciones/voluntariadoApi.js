import { apiGet, apiPatch, apiPost } from '../../shared/apiClient.js';

const VOLUNTEERS_PATH = '/api/voluntarios';

export function getVolunteers(filters = {}) {
  const query = new URLSearchParams(Object.entries(filters).filter(([, value]) => value));
  const suffix = query.size ? `?${query}` : '';
  return apiGet(`${VOLUNTEERS_PATH}${suffix}`);
}

export function createVolunteer(data) {
  return apiPost(VOLUNTEERS_PATH, data, { modulo: 'voluntariado' });
}

export function updateVolunteerStatus(id, status) {
  return apiPatch(`${VOLUNTEERS_PATH}/${id}`, { status });
}
