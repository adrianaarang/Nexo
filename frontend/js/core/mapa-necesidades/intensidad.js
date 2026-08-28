/**
 * ==========================================
 * NEXO - INTENSIDAD DE NECESIDADES
 * Persona 4
 * ==========================================
 *
 * 0 - 5   → Verde
 * 6 - 15  → Naranja
 * 16+     → Rojo
 */


const INTENSIDADES = {

    baja: {
        nombre: "Baja",
        color: "#22c55e"
    },

    media: {
        nombre: "Moderada",
        color: "#f97316"
    },

    alta: {
        nombre: "Alta",
        color: "#ef4444"
    }

};


/**
 * Determina el color según
 * la cantidad de necesidades.
 */

function obtenerIntensidad(cantidad) {

    if (cantidad <= 5) {

        return INTENSIDADES.baja;

    }


    if (cantidad <= 15) {

        return INTENSIDADES.media;

    }


    return INTENSIDADES.alta;

}


export {
    INTENSIDADES,
    obtenerIntensidad
};