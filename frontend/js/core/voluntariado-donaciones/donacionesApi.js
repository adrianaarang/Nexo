// Donations API calls.
// Llamadas a la API de donaciones.
// En local usa FastAPI en el puerto 8000. En producción, el HTML puede definir
// window.NEXO_API_BASE = "" para usar rutas relativas detrás de un proxy.
const API_BASE = window.NEXO_API_BASE ?? "http://localhost:8000";

export async function getDonations(type = null) {
  const params = type ? `?tipo=${type}` : "";
  const resp = await fetch(`${API_BASE}/api/donaciones${params}`);
  if (!resp.ok) throw new Error(`GET /api/donaciones -> ${resp.status}`);
  return resp.json();
}

export async function postDonation(data) {
  const resp = await fetch(`${API_BASE}/api/donaciones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!resp.ok) throw new Error(`POST /api/donaciones -> ${resp.status}`);
  return resp.json();
}

export async function markDonationAsDelivered(id) {
  const resp = await fetch(`${API_BASE}/api/donaciones/${id}/estado`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ estado: "entregada" }),
  });
  if (!resp.ok) throw new Error(`PATCH /api/donaciones/${id}/estado -> ${resp.status}`);
  return resp.json();
}
