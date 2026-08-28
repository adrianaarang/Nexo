import {
  API_BASE_URL,
  apiGet,
  apiPost,
} from '../../shared/apiClient.js';

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
  const response = await fetch(
    `${API_BASE_URL}${VOLUNTEERS_PATH}/${id}`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status }),
    }
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      data?.detalle ||
      `No se pudo actualizar el estado (${response.status}).`
    );
  }

  return data;
}