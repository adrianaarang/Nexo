// Punto único por el que pasan todas las llamadas a la API de Nexo.
// Parte de la base común: cada equipo importa apiGet/apiPost en vez de
// usar fetch() directamente, para que la cola offline funcione igual
// en todos los módulos.
//
// Si un POST falla por falta de red, encola la acción (ver
// js/siguiente/modo-offline/syncQueue.js, del Equipo 4) en vez de
// perder el dato del usuario.

import { encolarAccion } from "../siguiente/modo-offline/syncQueue.js";

export const API_BASE_URL = "http://127.0.0.1:8000";

export async function apiGet(path) {
  const resp = await fetch(`${API_BASE_URL}${path}`);
  if (!resp.ok) throw new Error(`GET ${path} -> ${resp.status}`);
  return resp.json();
}

export async function apiPost(path, body, { modulo } = {}) {
  try {
    const resp = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!resp.ok) throw new Error(`POST ${path} -> ${resp.status}`);
    return await resp.json();
  } catch (err) {
    if (modulo) {
      await encolarAccion(modulo, body);
      return { _offline: true, ...body };
    }
    throw err;
  }
}
