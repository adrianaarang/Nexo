// frontend/js/core/mapa-necesidades/formularioNecesidad.js
import { crearNecesidad, configurarBaseUrl } from "./necesidadesApi.js";

// Si trabajas localmente con Live Server (puerto 5500) y FastAPI en 8000:
configurarBaseUrl("http://localhost:8000/api/necesidades");

export class NeedFormController {
  constructor(container, onSubmit) {
    this.container =
      typeof container === "string"
        ? document.querySelector(container)
        : container;
    this.onSubmit = onSubmit;
    this.formElement = null;
    this.init();
  }

  init() {
    if (!this.container) return;
    this.formElement =
      this.container.tagName === "FORM"
        ? this.container
        : this.container.querySelector("form");

    if (this.formElement) {
      this.bindEvents();
      this.setupGeolocation();
    }
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
        (position) => {
          const { latitude, longitude } = position.coords;
          this.setCoordinates(latitude, longitude);
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

  setCoordinates(lat, lng) {
    const latInput =
      this.formElement.querySelector("#input-lat") ||
      this.formElement.querySelector("#needLat");
    const lngInput =
      this.formElement.querySelector("#input-lng") ||
      this.formElement.querySelector("#needLng");

    if (latInput && lngInput) {
      latInput.value = Number(lat).toFixed(6);
      lngInput.value = Number(lng).toFixed(6);
    }
  }

  bindEvents() {
    this.formElement.addEventListener("submit", async (e) => {
      e.preventDefault();

      const titleInput =
        this.formElement.querySelector("#input-titulo") ||
        this.formElement.querySelector("#needTitle");
      const typeSelect =
        this.formElement.querySelector("#select-tipo") ||
        this.formElement.querySelector("#needType");
      const prioritySelect =
        this.formElement.querySelector("#select-prioridad") ||
        this.formElement.querySelector("#needPriority");
      const descTextarea =
        this.formElement.querySelector("#textarea-desc") ||
        this.formElement.querySelector("#needDescription");
      const latInput =
        this.formElement.querySelector("#input-lat") ||
        this.formElement.querySelector("#needLat");
      const lngInput =
        this.formElement.querySelector("#input-lng") ||
        this.formElement.querySelector("#needLng");

      const payloadSpanish = {
        titulo: titleInput ? titleInput.value.trim() : "",
        tipo: typeSelect ? typeSelect.value : "alimento",
        descripcion: descTextarea ? descTextarea.value.trim() : "",
        latitud: parseFloat(latInput?.value),
        longitud: parseFloat(lngInput?.value),
        prioridad: prioritySelect ? prioritySelect.value : "media",
      };

      if (isNaN(payloadSpanish.latitud) || isNaN(payloadSpanish.longitud)) {
        alert(
          "Por favor, selecciona un punto en el mapa o usa la geolocalización.",
        );
        return;
      }

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
  }
}
