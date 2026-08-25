import { API_BASE_URL, apiGet, apiPost } from '../../shared/apiClient.js';

const VOLUNTEERS_PATH = '/api/voluntarios';

export function getVolunteers(filters = {}) {
  const query = new URLSearchParams(Object.entries(filters).filter(([, value]) => value));
  const suffix = query.size ? `?${query}` : '';
  return apiGet(`${VOLUNTEERS_PATH}${suffix}`);
}

export function createVolunteer(data) {
  return apiPost(VOLUNTEERS_PATH, data, { modulo: 'voluntariado' });
}

export async function updateVolunteerStatus(id, status) {
  const resp = await fetch(`${API_BASE_URL}${VOLUNTEERS_PATH}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
  if (!resp.ok) {
    throw new Error(`PATCH ${VOLUNTEERS_PATH}/${id} -> ${resp.status}`);
  }
  return resp.json();
}
