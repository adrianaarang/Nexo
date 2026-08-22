import { apiGet, apiPost } from "../../shared/apiClient.js";

export async function getDonaciones(tipo = null) {
  const params = tipo ? `?tipo=${tipo}` : "";
  return apiGet(`/api/donaciones${params}`);
}

export async function postDonacion(datos) {
  return apiPost("/api/donaciones", datos, { modulo: "donaciones" });
}
