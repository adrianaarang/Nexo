/**
 * probar_integracion_necesidades.mjs
 *
 * Prueba de integración manual de punta a punta para el módulo de
 * necesidades: ejercita necesidadesApi.js contra un backend FastAPI
 * corriendo de verdad (no mocks), cubriendo los casos felices y los
 * de error que definen el contrato en schemas.py / routes.py.
 *
 * Uso:
 *   1. Levanta el backend (por ejemplo: uvicorn main:app --reload).
 *   2. node probar_integracion_necesidades.mjs
 *      (o: BASE_URL=http://localhost:8001/api/necesidades node probar_integracion_necesidades.mjs)
 *
 * Requiere Node 18+ (fetch nativo) y que necesidadesApi.js esté en el
 * mismo directorio o se ajuste el import de abajo a su ruta real:
 *   frontend/js/core/mapa-necesidades/necesidadesApi.js
 *
 * El script NO usa un framework de test (no añade dependencias);
 * imprime PASS/FAIL por caso y un resumen final, con código de salida
 * distinto de 0 si algo falla, para poder engancharlo a CI más adelante.
 */

import {
  configurarBaseUrl,
  obtenerNecesidades,
  crearNecesidad,
  actualizarEstadoNecesidad,
  NecesidadApiError,
  TIPOS_NECESIDAD,
  PRIORIDADES_NECESIDAD,
  ESTADOS_NECESIDAD,
} from "./necesidadesApi.js";

const BASE_URL = process.env.BASE_URL || "http://localhost:8000/api/necesidades";
configurarBaseUrl(BASE_URL);

// --- utilidades mínimas de test -------------------------------------------

let pasadas = 0;
let falladas = 0;

/**
 * Ejecuta un caso de prueba, capturando cualquier excepción como fallo.
 * @param {string} nombre
 * @param {() => Promise<void>} fn
 */
async function caso(nombre, fn) {
  try {
    await fn();
    console.log(`  ✅ ${nombre}`);
    pasadas += 1;
  } catch (err) {
    console.log(`  ❌ ${nombre}`);
    console.log(`     ${err.message}`);
    falladas += 1;
  }
}

function assert(condicion, mensaje) {
  if (!condicion) throw new Error(mensaje);
}

/**
 * Espera que fn lance NecesidadApiError con el status indicado.
 * @param {() => Promise<any>} fn
 * @param {number} statusEsperado
 * @returns {Promise<NecesidadApiError>}
 */
async function esperarError(fn, statusEsperado) {
  try {
    await fn();
  } catch (err) {
    if (!(err instanceof NecesidadApiError)) {
      throw new Error(`Se esperaba NecesidadApiError, llegó: ${err.name}: ${err.message}`);
    }
    if (err.status !== statusEsperado) {
      throw new Error(
        `Se esperaba status ${statusEsperado}, llegó ${err.status} (${err.detalle ?? "sin detalle"})`
      );
    }
    return err;
  }
  throw new Error(`Se esperaba que lanzara un error ${statusEsperado} y no lanzó nada`);
}

function coordenadasDeSondeo() {
  // Coordenadas de relleno válidas (Madrid). No representan un lugar real
  // de necesidad; son solo datos de prueba.
  return { latitud: 40.4168, longitud: -3.7038 };
}

// --- casos de prueba --------------------------------------------------------

async function main() {
  console.log(`\nProbando contrato de la API de necesidades en ${BASE_URL}\n`);

  let necesidadCreada = null;

  console.log("Creación (POST):");

  await caso("crea una necesidad válida con todos los campos", async () => {
    const { latitud, longitud } = coordenadasDeSondeo();
    const resultado = await crearNecesidad({
      titulo: "Prueba de integración — agua potable",
      tipo: TIPOS_NECESIDAD.AGUA,
      descripcion: "Necesidad creada por el script de pruebas manuales.",
      direccion: "Puerta del Sol, Madrid",
      latitud,
      longitud,
      prioridad: PRIORIDADES_NECESIDAD.ALTA,
    });

    assert(typeof resultado.id === "number", "falta 'id' numérico en la respuesta");
    assert(resultado.estado === ESTADOS_NECESIDAD.ABIERTA, "el estado inicial debería ser 'abierta'");
    assert(resultado.tipo === TIPOS_NECESIDAD.AGUA, "el campo 'tipo' no coincide con lo enviado");
    assert(resultado.direccion === "Puerta del Sol, Madrid", "el campo 'direccion' no coincide con lo enviado");
    assert(typeof resultado.creado_en === "string", "falta 'creado_en' en la respuesta");

    necesidadCreada = resultado;
  });

  await caso("aplica 'media' como prioridad por defecto si se omite", async () => {
    const { latitud, longitud } = coordenadasDeSondeo();
    const resultado = await crearNecesidad({
      titulo: "Prueba de integración — sin prioridad",
      tipo: TIPOS_NECESIDAD.ALIMENTOS,
      descripcion: "Verifica el valor por defecto de prioridad.",
      latitud,
      longitud,
      // prioridad omitida a propósito
    });

    assert(
      resultado.prioridad === PRIORIDADES_NECESIDAD.MEDIA,
      `se esperaba prioridad 'media' por defecto, llegó '${resultado.prioridad}'`
    );
  });

  await caso("genera un título a partir de la categoría si se omite (formulario simplificado)", async () => {
    const { latitud, longitud } = coordenadasDeSondeo();
    const resultado = await crearNecesidad({
      tipo: TIPOS_NECESIDAD.PARAFARMACIA,
      latitud,
      longitud,
      // titulo, descripcion y direccion omitidos a propósito
    });

    assert(
      resultado.titulo.length > 0,
      "el servidor debería generar un título aunque el formulario no lo mande"
    );
    assert(
      resultado.categoria_etiqueta === "💊 Parafarmacia",
      `se esperaba la etiqueta con emoji de parafarmacia, llegó '${resultado.categoria_etiqueta}'`
    );
    assert(
      resultado.direccion === "",
      "la dirección debería quedar vacía si no se manda (solo hay coordenadas)"
    );
  });

  console.log("\nValidación (422 — errores de schemas.py):");

  await caso("rechaza latitud fuera de rango con 422", async () => {
    const err = await esperarError(
      () =>
        crearNecesidad({
          titulo: "Latitud inválida",
          tipo: TIPOS_NECESIDAD.AGUA,
          descripcion: "Debe fallar por rango.",
          latitud: 999,
          longitud: -3.7038,
        }),
      422
    );
    assert(err.detalle, "el error 422 debería traer un 'detalle' legible del campo que falló");
  });

  await caso("rechaza un 'tipo' fuera del enum con 422", async () => {
    await esperarError(
      () =>
        crearNecesidad({
          titulo: "Tipo inválido",
          tipo: "combustible", // no existe en NeedType
          descripcion: "Debe fallar por enum.",
          ...coordenadasDeSondeo(),
        }),
      422
    );
  });

  await caso("rechaza una clave extra en el body con 422 (extra=forbid)", async () => {
    await esperarError(
      () =>
        crearNecesidad({
          titulo: "Clave extra",
          tipo: TIPOS_NECESIDAD.AGUA,
          descripcion: "Debe fallar por clave no reconocida.",
          ...coordenadasDeSondeo(),
          contacto: "600000000", // no forma parte del contrato
        }),
      422
    );
  });

  console.log("\nListado (GET):");

  await caso("lista todas las necesidades sin filtros", async () => {
    const lista = await obtenerNecesidades();
    assert(Array.isArray(lista), "la respuesta de GET debería ser un array");
    assert(
      lista.some((n) => n.id === necesidadCreada.id),
      "la necesidad recién creada debería aparecer en el listado"
    );
  });

  await caso("filtra por tipo y devuelve solo ese tipo", async () => {
    const lista = await obtenerNecesidades({ tipo: TIPOS_NECESIDAD.AGUA });
    assert(
      lista.every((n) => n.tipo === TIPOS_NECESIDAD.AGUA),
      "el filtro por 'tipo' devolvió elementos de otro tipo"
    );
  });

  await caso("filtra por estado y devuelve solo ese estado", async () => {
    const lista = await obtenerNecesidades({ estado: ESTADOS_NECESIDAD.ABIERTA });
    assert(
      lista.every((n) => n.estado === ESTADOS_NECESIDAD.ABIERTA),
      "el filtro por 'estado' devolvió elementos con otro estado"
    );
  });

  console.log("\nCambio de estado (PATCH) — ciclo de vida simplificado a un solo paso:");

  await caso("repetir el estado actual ('abierta') es idempotente (no lanza error)", async () => {
    const actualizada = await actualizarEstadoNecesidad(
      necesidadCreada.id,
      ESTADOS_NECESIDAD.ABIERTA
    );
    assert(actualizada.estado === ESTADOS_NECESIDAD.ABIERTA, "repetir el estado actual debería ser un no-op válido");
  });

  await caso("avanza de 'abierta' a 'cubierta'", async () => {
    const actualizada = await actualizarEstadoNecesidad(
      necesidadCreada.id,
      ESTADOS_NECESIDAD.CUBIERTA
    );
    assert(actualizada.estado === ESTADOS_NECESIDAD.CUBIERTA, "el estado no avanzó a 'cubierta'");
  });

  await caso("rechaza reabrir una necesidad ya 'cubierta' con 409", async () => {
    await esperarError(
      () => actualizarEstadoNecesidad(necesidadCreada.id, ESTADOS_NECESIDAD.ABIERTA),
      409
    );
  });

  console.log("\nCasos no encontrados (404):");

  await caso("PATCH sobre un id inexistente devuelve 404", async () => {
    await esperarError(
      () => actualizarEstadoNecesidad(999999, ESTADOS_NECESIDAD.CUBIERTA),
      404
    );
  });

  // --- resumen ---------------------------------------------------------

  console.log(`\n${"-".repeat(50)}`);
  console.log(`Resultado: ${pasadas} pasadas, ${falladas} fallidas de ${pasadas + falladas}`);
  console.log(`${"-".repeat(50)}\n`);

  if (falladas > 0) {
    process.exitCode = 1;
  }
}

main().catch((err) => {
  console.error("\nEl script no pudo completarse:", err);
  console.error(
    `¿Está el backend levantado en ${BASE_URL}? Prueba: BASE_URL=http://localhost:PUERTO/api/necesidades node probar_integracion_necesidades.mjs\n`
  );
  process.exitCode = 1;
});
