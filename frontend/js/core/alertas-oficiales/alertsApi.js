// API client for official alerts (Grupo 2 - Juan). B1.
// Uses the shared apiGet from the base common so offline queueing works.
// Params must match backend GET /api/alertas (tipo, severidad, pais).
import { apiGet } from '../../shared/apiClient.js';

export async function getAlerts({ tipo, severidad, pais } = {}) {
  const params = new URLSearchParams();
  if (tipo) params.set('tipo', tipo);
  if (severidad) params.set('severidad', severidad);
  if (pais) params.set('pais', pais);
  const query = params.toString();
  return apiGet('/api/alertas?' + (query ? query : ''));
}
