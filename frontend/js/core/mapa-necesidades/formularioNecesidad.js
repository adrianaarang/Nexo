// frontend/js/core/mapa-necesidades/formularioNecesidad.js
import { crearNecesidad, configurarBaseUrl } from "./necesidadesApi.js";
import { buscarDireccion, direccionInversa } from "./geocodificacion.js";

// Si trabajas localmente con Live Server (puerto 5500) y FastAPI en 8000:
configurarBaseUrl("http://localhost:8000/api/necesidades");

/**
 * Formulario simplificado de "Reportar necesidad" (rediseño Grupo 1).
 *
 * Registrar una necesidad exige solo dos cosas: elegir una de las 8
 * categorías cerradas (botones con emoji) y decir dónde. La ubicación
 * se puede fijar de tres formas, todas equivalentes:
 *   1. Escribiendo la dirección a mano (se geocodifica al enviar).
 *   2. Pulsando "Usar mi ubicación" (GPS; se traduce a una dirección
 *      legible mediante geocodificación inversa).
 *   3. Haciendo clic en el mapa (mapaNecesidades.js; también se traduce
 *      a una dirección legible).
 *
 * No hay campo de título: el backend genera uno a partir de la
 * categoría (ver services.py). La descripción es el único texto libre
 * que rellena la persona, y es opcional.
 */
export class NeedFormController {
  constructor(container, onSubmit) {
    this.container =
      typeof container === "string"
        ? document.querySelector(container)
        : container;
    this.onSubmit = onSubmit;
    this.formElement = null;
    this.tipoSeleccionado = null;
    // Coordenadas ya confirmadas por GPS o clic en el mapa. Si la persona
    // edita el campo de dirección a mano después, se invalidan (ver
    // setupDireccion) y se geocodifican de nuevo al enviar el formulario.
    this.coordenadasConfirmadas = null;
    this.init();
  }

  init() {
    if (!this.container) return;
    this.formElement =
      this.container.tagName === "FORM"
        ? this.container
        : this.container.querySelector("form");

    if (this.formElement) {
      this.setupCategorias();
      this.setupDireccion();
      this.bindEvents();
      this.setupGeolocation();
      this.setupClicEnMapa();
    }
  }

  /**
   * Convierte el grupo de botones .nexo-categoria-btn (data-tipo) en el
   * selector de categoría cerrada. Sustituye al antiguo <select id="select-tipo">.
   */
  setupCategorias() {
    const botones = this.formElement.querySelectorAll(".nexo-categoria-btn");
    if (!botones.length) return;

    botones.forEach((boton) => {
      boton.setAttribute("aria-pressed", "false");
      boton.addEventListener("click", () => {
        botones.forEach((b) => {
          b.classList.remove("is-selected");
          b.setAttribute("aria-pressed", "false");
        });
        boton.classList.add("is-selected");
        boton.setAttribute("aria-pressed", "true");
        this.tipoSeleccionado = boton.dataset.tipo;
      });
    });

    // Preseleccionamos la primera categoría para que el formulario
    // funcione igual de rápido si la persona no toca los botones.
    const primero = botones[0];
    primero.classList.add("is-selected");
    primero.setAttribute("aria-pressed", "true");
    this.tipoSeleccionado = primero.dataset.tipo;
  }

  /**
   * Si la persona escribe o edita la dirección a mano, invalidamos las
   * coordenadas que hubiera confirmadas por GPS/clic: al enviar el
   * formulario se geocodificará el texto actual, no las coordenadas viejas.
   *
   * Importante: esto solo salta con tecleo real de la persona ("input"),
   * no cuando este mismo controlador rellena el campo por su cuenta tras
   * el GPS o un clic en el mapa (asignar `.value` en JS no dispara "input").
   */
  setupDireccion() {
    const direccionInput = this.formElement.querySelector("#input-direccion");
    if (!direccionInput) return;

    direccionInput.addEventListener("input", () => {
      this.coordenadasConfirmadas = null;
    });
  }

  setupGeolocation() {
    const gpsBtn = this.formElement.querySelector("#btn-usar-gps");
    if (!gpsBtn) return;

    gpsBtn.addEventListener("click", () => {
      if (!navigator.geolocation) {
        alert("Tu navegador no soporta geolocalización.");
        return;
      }
      gpsBtn.textContent = "⏳ Obteniendo ubicación...";
      gpsBtn.disabled = true;

      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          await this.confirmarUbicacion(latitude, longitude);
          gpsBtn.textContent = "✓ Ubicación capturada";
          setTimeout(() => {
            gpsBtn.textContent = "📍 Usar mi ubicación";
            gpsBtn.disabled = false;
          }, 2000);
        },
        () => {
          alert("No se pudo obtener tu ubicación.");
          gpsBtn.textContent = "📍 Usar mi ubicación";
          gpsBtn.disabled = false;
        },
        { enableHighAccuracy: true, timeout: 10000 },
      );
    });
  }

  /**
   * Segunda vía para fijar la ubicación (además del GPS): un clic en el
   * mapa. mapaNecesidades.js dispara este evento con las coordenadas
   * pulsadas; aquí solo escuchamos, sin importar directamente ese módulo.
   */
  setupClicEnMapa() {
    document.addEventListener("nexo:ubicacion-seleccionada", async (evento) => {
      const { lat, lng } = evento.detail || {};
      if (typeof lat === "number" && typeof lng === "number") {
        await this.confirmarUbicacion(lat, lng);
      }
    });
  }

  /**
   * Punto común para GPS y clic en el mapa: guarda las coordenadas como
   * "confirmadas" (no habrá que volver a geocodificarlas al enviar) y
   * rellena el campo de dirección con su traducción legible, si la hay.
   */
  async confirmarUbicacion(lat, lng) {
    this.coordenadasConfirmadas = { lat, lng };

    const direccionInput = this.formElement.querySelector("#input-direccion");
    if (!direccionInput) return;

    const direccionLegible = await direccionInversa(lat, lng);
    // Si Nominatim no devuelve nada legible, dejamos las coordenadas en
    // crudo: seguimos teniendo ubicación válida aunque no haya texto bonito.
    direccionInput.value =
      direccionLegible || `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
  }

  bindEvents() {
    this.formElement.addEventListener("submit", async (e) => {
      e.preventDefault();

      if (!this.tipoSeleccionado) {
        alert("Selecciona qué necesitas.");
        return;
      }

      const direccionInput = this.formElement.querySelector("#input-direccion");
      const descTextarea =
        this.formElement.querySelector("#textarea-desc") ||
        this.formElement.querySelector("#needDescription");
      const textoDireccion = direccionInput ? direccionInput.value.trim() : "";

      const submitBtn = this.formElement.querySelector('button[type="submit"]');

      let lat;
      let lng;
      let direccionParaGuardar = textoDireccion;

      if (this.coordenadasConfirmadas) {
        // Vino de GPS o de un clic en el mapa: ya tenemos coordenadas
        // exactas, no hace falta geocodificar nada.
        ({ lat, lng } = this.coordenadasConfirmadas);
      } else if (textoDireccion) {
        // La persona ha escrito (o editado) la dirección a mano: hay que
        // geocodificarla antes de poder guardar la necesidad.
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = "Buscando dirección...";
        }

        try {
          const resultado = await buscarDireccion(textoDireccion);

          if (!resultado) {
            alert(
              "No hemos encontrado esa dirección. Prueba a escribirla de otra forma, usar tu ubicación o hacer clic en el mapa.",
            );
            return;
          }

          lat = resultado.lat;
          lng = resultado.lng;
          direccionParaGuardar = resultado.direccion;
        } catch (error) {
          console.error("Error geocodificando la dirección:", error);
          alert(
            "No hemos podido buscar esa dirección ahora mismo. Prueba a usar tu ubicación o hacer clic en el mapa.",
          );
          return;
        } finally {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = "Publicar Necesidad";
          }
        }
      } else {
        alert(
          "Escribe una dirección, usa tu ubicación o haz clic en el mapa para decir dónde.",
        );
        return;
      }

      // titulo se envía vacío: el backend genera uno a partir de la
      // categoría (ver services.py). descripcion es opcional.
      const payloadSpanish = {
        titulo: "",
        tipo: this.tipoSeleccionado,
        descripcion: descTextarea ? descTextarea.value.trim() : "",
        direccion: direccionParaGuardar,
        latitud: lat,
        longitud: lng,
      };

      try {
        // Enviar al backend centralizado y recuperar el objeto completo con ID real
        const nuevaNecesidad = await crearNecesidad(payloadSpanish);

        if (typeof this.onSubmit === "function") {
          this.onSubmit(nuevaNecesidad);
        }

        this.reset();
        alert("¡Necesidad registrada correctamente!");
      } catch (error) {
        console.error("Error guardando necesidad:", error);
        alert(
          `Error: ${error.message} ${error.detalle ? `(${error.detalle})` : ""}`,
        );
      }
    });
  }

  reset() {
    if (this.formElement) this.formElement.reset();
    this.coordenadasConfirmadas = null;
    this.setupCategorias();
  }
}
