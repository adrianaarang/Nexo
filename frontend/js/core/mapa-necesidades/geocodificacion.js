/**
 * geocodificacion.js
 *
 * Convierte entre una dirección escrita a mano y las coordenadas que
 * necesita el backend (latitud/longitud), usando Nominatim (el buscador
 * de OpenStreetMap, el mismo proyecto que las teselas del mapa).
 *
 * - buscarDireccion(texto): dirección escrita -> {lat, lng, direccion}
 *   Se usa cuando la persona escribe la dirección a mano.
 * - direccionInversa(lat, lng): coordenadas -> texto de dirección
 *   Se usa tras el GPS o un clic en el mapa, para mostrar algo legible
 *   en vez de números sueltos.
 *
 * Nota: Nominatim es un servicio gratuito pensado para uso razonable
 * (más o menos 1 petición/segundo, sin ráfagas). Sirve perfectamente
 * para esta demo, pero el navegador no puede fijar la cabecera
 * "User-Agent" que pide su política de uso; para producción real lo
 * correcto sería pasar estas llamadas por un proxy en el propio
 * backend, con caché y un User-Agent identificable.
 */

const NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org";

/**
 * Busca una dirección escrita a mano y devuelve su mejor coincidencia.
 *
 * @param {string} texto - p. ej. "Calle Mayor 3, Valencia"
 * @returns {Promise<{lat: number, lng: number, direccion: string}|null>}
 *   null si no hay ninguna coincidencia (no es un error, solo "no encontrado").
 * @throws {Error} si no se puede contactar con el servicio (red caída, etc.)
 */
export async function buscarDireccion(texto) {
  const consulta = (texto || "").trim();
  if (!consulta) return null;

  const url = `${NOMINATIM_BASE_URL}/search?format=json&limit=1&q=${encodeURIComponent(consulta)}`;

  let response;
  try {
    response = await fetch(url, { headers: { Accept: "application/json" } });
  } catch (_err) {
    throw new Error("No se pudo contactar con el buscador de direcciones.");
  }

  if (!response.ok) {
    throw new Error("El buscador de direcciones no respondió correctamente.");
  }

  const resultados = await response.json();
  if (!Array.isArray(resultados) || resultados.length === 0) {
    return null;
  }

  const { lat, lon, display_name: direccion } = resultados[0];
  return { lat: parseFloat(lat), lng: parseFloat(lon), direccion };
}

/**
 * Traduce unas coordenadas a una dirección legible (geocodificación inversa).
 *
 * @param {number} lat
 * @param {number} lng
 * @returns {Promise<string|null>} la dirección legible, o null si falla
 *   (fallo silencioso a propósito: si no hay dirección legible, seguimos
 *   teniendo las coordenadas, que son lo único que exige el backend).
 */
export async function direccionInversa(lat, lng) {
  const url = `${NOMINATIM_BASE_URL}/reverse?format=json&lat=${lat}&lon=${lng}`;

  try {
    const response = await fetch(url, { headers: { Accept: "application/json" } });
    if (!response.ok) return null;

    const resultado = await response.json();
    return resultado?.display_name || null;
  } catch (_err) {
    return null;
  }
}
