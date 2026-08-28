/**
 * ==========================================
 * NEXO - MARCADORES DE NECESIDADES
 * Persona 4
 * ==========================================
 */

const ICONOS_NECESIDADES = {
    water: "💧",
    food: "🥫",
    medication: "🩹",
    clothing: "👕",
    hygiene: "🧴",
    shelter: "🏠",
    transport: "🚗"
};


const NOMBRES_NECESIDADES = {
    water: "Agua",
    food: "Enlatados",
    medication: "Primeros auxilios / parafarmacia",
    clothing: "Ropa",
    hygiene: "Higiene",
    shelter: "Refugio",
    transport: "Transporte"
};


/**
 * Crea el marcador.
 *
 * El emoji indica el tipo.
 * El color indica la intensidad.
 */

function crearIconoNecesidad(
    tipo,
    color = "#22c55e"
) {

    const emoji =
        ICONOS_NECESIDADES[tipo] || "📦";


    return L.divIcon({

        className: "nexo-marker",

        html: `
            <div
                class="nexo-marker-icon"
                style="background-color: ${color};"
            >
                ${emoji}
            </div>
        `,

        iconSize: [42, 42],

        iconAnchor: [21, 21],

        popupAnchor: [0, -21]

    });

}


/**
 * Devuelve el nombre legible
 * de la necesidad.
 */

function obtenerNombreNecesidad(tipo) {

    return (
        NOMBRES_NECESIDADES[tipo]
        || "Otros"
    );

}


export {
    crearIconoNecesidad,
    obtenerNombreNecesidad
};