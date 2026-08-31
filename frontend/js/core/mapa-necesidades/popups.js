/**
 * ==========================================
 * NEXO - POPUPS DE NECESIDADES
 * ==========================================
 */

import {
    obtenerNombreNecesidad
} from "./marcadores.js";


function crearPopupNecesidad(
    necesidad
) {

    const nombre =
        obtenerNombreNecesidad(
            necesidad.type
        );


    const estado =
        necesidad.status === "open"
            ? "Abierta"
            : "Cubierta";


    /*
     * Si el mock tiene quantity, se usa esa cantidad.
     * Si no existe, se muestra 1.
     */

    const cantidad =
        necesidad.quantity ??
        necesidad.people ??
        1;


    return `
        <div class="nexo-popup">

            <h3>
                🆘 ${nombre}
            </h3>

            <p>
                <strong>Cantidad:</strong>
                ${cantidad}
                ${cantidad === 1
                    ? "persona"
                    : "personas"}
            </p>

            <p>
                <strong>Estado:</strong>
                ${estado}
            </p>

        </div>
    `;
}


export {
    crearPopupNecesidad
};