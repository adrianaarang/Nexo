// Donations API calls — bypasses apiClient.js to avoid the broken syncQueue import chain.
// Llamadas a la API de donaciones — evita apiClient.js por la cadena rota de syncQueue.
const API_BASE = "http://localhost:8000";

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
