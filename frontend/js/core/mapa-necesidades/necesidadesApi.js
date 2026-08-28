/**
 * necesidadesApi.js
 *
 * Capa de conexión con el backend para el módulo de necesidades.
 * Responsabilidad única: llamar a /api/necesidades y devolver datos
 * ya parseados (o lanzar errores ya normalizados) para que el resto
 * del frontend (mapa, formularios, listados) no tenga que saber nada
 * de fetch, JSON.stringify ni códigos HTTP.
 *
 * Contrato esperado con el backend (routes.py / schemas.py) — rediseño con
 * 8 categorías cerradas, ciclo de vida simplificado a abierta/cubierta y
 * ubicación por dirección (geocodificada) en vez de coordenadas sueltas:
 *
 *   GET    /api/necesidades?tipo=&estado=   -> Necesidad[]
 *   GET    /api/necesidades/{id}            -> Necesidad
 *   POST   /api/necesidades                 -> Necesidad (201)
 *   PATCH  /api/necesidades/{id}            -> Necesidad (200)
 *
 *   Necesidad = {
 *     id: number,
 *     titulo: string,             // generado por el servidor a partir de la categoría
 *     tipo: string,                // una de TIPOS_NECESIDAD
 *     descripcion: string,         // opcional, puede venir vacía
 *     direccion: string,           // texto legible del lugar (geocodificacion.js)
 *     latitud: number,
 *     longitud: number,
 *     prioridad: string,
 *     estado: "abierta" | "cubierta",
 *     creado_en: string,           // fecha ISO generada por el servidor
 *     categoria_etiqueta: string   // p. ej. "💧 Agua", lista para pintar
 *   }
 *
 *   Errores -> siempre { error: string, detalle: string } con status 404 o 409.
 *
 * Si alguno de estos nombres de campo o valores de enum no coincide
 * exactamente con lo que Persona 1/2 implementen, es aquí donde va a
 * fallar primero: revisa NECESIDADES_ENDPOINTS abajo y los nombres de
 * las claves en los payloads.
 */

// "let" en vez de "const" para poder apuntar a una URL absoluta desde
// pruebas manuales en Node (donde no hay origen implícito como en el
// navegador). En producción, dentro del navegador, no hace falta tocarlo:
// la ruta relativa funciona porque frontend y backend comparten origen.
let NECESIDADES_BASE_URL = "/api/necesidades";

/**
 * Sobrescribe la URL base de la API. Pensado para scripts de prueba
 * manual (Node) o para desarrollo local si el backend corre en otro
 * puerto sin proxy configurado.
 *
 * @param {string} baseUrl - p. ej. "http://localhost:8000/api/necesidades"
 */
export function configurarBaseUrl(baseUrl) {
  NECESIDADES_BASE_URL = baseUrl;
}

// Enums espejo de schemas.py (NeedType, NeedPriority, NeedStatus).
// Mantenerlos aquí evita strings sueltos repartidos por selects/formularios
// y hace explícito el punto de contacto si el backend cambia un valor.
//
// 8 categorías cerradas del rediseño (antes había 6, con "medicina" y
// "herramientas" en vez de "parafarmacia", "ropa", "higiene" y "otros").
export const TIPOS_NECESIDAD = Object.freeze({
  AGUA: "agua",
  ALIMENTOS: "alimentos",
  PARAFARMACIA: "parafarmacia",
  ROPA: "ropa",
  HIGIENE: "higiene",
  REFUGIO: "refugio",
  TRANSPORTE: "transporte",
  OTROS: "otros",
});

// Etiqueta con emoji por categoría. El backend ya la manda en
// "categoria_etiqueta" dentro de cada Necesidad; esta copia sirve para
// pintar los propios controles del formulario/filtro (que no vienen del
// backend, los define este archivo) sin repetir los emojis sueltos.
export const ETIQUETAS_TIPO_NECESIDAD = Object.freeze({
  [TIPOS_NECESIDAD.AGUA]: "💧 Agua",
  [TIPOS_NECESIDAD.ALIMENTOS]: "🍞 Alimentos",
  [TIPOS_NECESIDAD.PARAFARMACIA]: "💊 Parafarmacia",
  [TIPOS_NECESIDAD.ROPA]: "👕 Ropa",
  [TIPOS_NECESIDAD.HIGIENE]: "🧴 Higiene",
  [TIPOS_NECESIDAD.REFUGIO]: "🏠 Refugio",
  [TIPOS_NECESIDAD.TRANSPORTE]: "🚗 Transporte",
  [TIPOS_NECESIDAD.OTROS]: "📦 Otros",
});

export const PRIORIDADES_NECESIDAD = Object.freeze({
  BAJA: "baja",
  MEDIA: "media",
  ALTA: "alta",
  CRITICA: "critica",
});

// Ciclo de vida simplificado a un solo paso (antes había un estado
// intermedio "en_proceso" que se ha retirado en este rediseño).
export const ESTADOS_NECESIDAD = Object.freeze({
  ABIERTA: "abierta",
  CUBIERTA: "cubierta",
});

/**
 * Error personalizado para poder distinguir en el código que consume
 * esta API entre "no encontrado" (404), "transición inválida" (409)
 * y errores inesperados (red, 500, JSON mal formado).
 */
class NecesidadApiError extends Error {
  /**
   * @param {string} mensaje
   * @param {number} status - código HTTP devuelto por el servidor
   * @param {string|null} detalle - campo "detalle" del JSON de error, si existe
   */
  constructor(mensaje, status, detalle = null) {
    super(mensaje);
    this.name = "NecesidadApiError";
    this.status = status;
    this.detalle = detalle;
  }
}

/**
 * Construye un mensaje legible a partir del formato de error estándar
 * de FastAPI para fallos de validación de Pydantic (422):
 *   { "detail": [ { "loc": [...], "msg": "...", "type": "..." }, ... ] }
 *
 * Este formato NO pasa por el {error, detalle} que routes.py construye
 * a mano para 404/409: los 422 los genera FastAPI automáticamente antes
 * de que el código del endpoint se ejecute (p. ej. "prioridad" con un
 * valor fuera del enum, "latitud" fuera de rango, o una clave extra en
 * el body, ya que NeedCreate usa extra="forbid").
 *
 * @param {any} cuerpo
 * @returns {string|null}
 */
function formatearDetalleValidacion(cuerpo) {
  if (!cuerpo || !Array.isArray(cuerpo.detail)) return null;

  return cuerpo.detail
    .map((err) => {
      const campo = Array.isArray(err.loc) ? err.loc.at(-1) : "campo";
      return `${campo}: ${err.msg}`;
    })
    .join("; ");
}

/**
 * Parsea la respuesta de fetch, lanzando NecesidadApiError si no es OK.
 *
 * Maneja dos formatos de error distintos que puede devolver el backend:
 *  - {error, detalle}: el formato propio del proyecto, usado a mano en
 *    routes.py para 404 (no encontrada) y 409 (transición inválida).
 *  - {detail: [...]}: el formato por defecto de FastAPI/Pydantic para
 *    422, cuando falla la validación de schemas.py antes de llegar
 *    al código del endpoint.
 *
 * @param {Response} response
 * @returns {Promise<any>} el JSON parseado si la respuesta fue exitosa
 */
async function parseRespuesta(response) {
  let cuerpo = null;

  try {
    cuerpo = await response.json();
  } catch (_err) {
    cuerpo = null;
  }

  if (!response.ok) {
    const detalleValidacion = formatearDetalleValidacion(cuerpo);

    const mensaje =
      (cuerpo && cuerpo.error) ||
      (detalleValidacion ? "Datos inválidos" : null) ||
      `Error inesperado (HTTP ${response.status})`;

    const detalle =
      (cuerpo && cuerpo.detalle) || detalleValidacion || null;

    throw new NecesidadApiError(mensaje, response.status, detalle);
  }

  return cuerpo;
}

/**
 * Construye la query string a partir de un objeto de filtros,
 * omitiendo claves undefined/null para no mandar "tipo=undefined".
 *
 * @param {{tipo?: string, estado?: string}} filtros
 * @returns {string}
 */
function construirQueryString(filtros = {}) {
  const params = new URLSearchParams();

  if (filtros.tipo != null) params.set("tipo", filtros.tipo);
  if (filtros.estado != null) params.set("estado", filtros.estado);

  const query = params.toString();
  return query ? `?${query}` : "";
}

/**
 * Obtiene las necesidades del mapa, con filtros opcionales por tipo y estado.
 *
 * @param {{tipo?: string, estado?: string}} [filtros]
 * @returns {Promise<Array<object>>}
 */
export async function obtenerNecesidades(filtros = {}) {
  const url = `${NECESIDADES_BASE_URL}${construirQueryString(filtros)}`;

  const response = await fetch(url, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  return parseRespuesta(response);
}

/**
 * Obtiene una única necesidad por su id (p. ej. al abrir el detalle
 * de un marcador del mapa).
 *
 * @param {number} idNecesidad
 * @returns {Promise<object>}
 */
export async function obtenerNecesidad(idNecesidad) {
  const response = await fetch(`${NECESIDADES_BASE_URL}/${idNecesidad}`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  return parseRespuesta(response);
}

/**
 * Crea una nueva necesidad en el mapa.
 *
 * El backend genera id, estado inicial ("abierta") y creado_en,
 * así que aquí solo enviamos los campos que rellena la persona usuaria.
 * "direccion" es el texto legible que el frontend obtiene al geocodificar
 * (ver geocodificacion.js); "titulo" puede llegar vacío y el servidor lo
 * genera a partir de la categoría (ver services.py).
 *
 * @param {{
 *   titulo?: string,
 *   tipo: string,
 *   descripcion?: string,
 *   direccion?: string,
 *   latitud: number,
 *   longitud: number,
 *   prioridad?: string
 * }} datosNecesidad
 * @returns {Promise<object>} la necesidad creada, tal como la devuelve el servidor
 */
export async function crearNecesidad(datosNecesidad) {
  const response = await fetch(NECESIDADES_BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(datosNecesidad),
  });

  return parseRespuesta(response);
}

/**
 * Cambia el estado de una necesidad existente.
 *
 * La única transición válida en el backend: abierta -> cubierta.
 * Un intento de reabrir una necesidad ya cubierta devuelve 409, que aquí
 * se traduce en un NecesidadApiError con status 409.
 *
 * @param {number} idNecesidad
 * @param {"abierta"|"cubierta"} nuevoEstado
 * @returns {Promise<object>} la necesidad actualizada
 */
export async function actualizarEstadoNecesidad(idNecesidad, nuevoEstado) {
  const response = await fetch(`${NECESIDADES_BASE_URL}/${idNecesidad}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ estado: nuevoEstado }),
  });

  return parseRespuesta(response);
}

export { NecesidadApiError };
