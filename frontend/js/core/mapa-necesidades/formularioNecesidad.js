// frontend/js/core/mapa-necesidades/formularioNecesidad.js

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

    // Si el contenedor ya es un formulario, lo usamos; si no, buscamos el formulario dentro
    this.formElement =
      this.container.tagName === "FORM"
        ? this.container
        : this.container.querySelector("form");

    if (this.formElement) {
      this.bindEvents();
      this.setupGeolocation();
    }
  }

  /**
   * Conecta la Geolocalización del navegador con los campos Latitud / Longitud
   */
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
        (error) => {
          console.error("Error obteniendo ubicación:", error);
          alert(
            "No se pudo obtener tu ubicación. Por favor, selecciona un punto en el mapa.",
          );
          gpsBtn.textContent = "📍 Usar mi ubicación";
          gpsBtn.disabled = false;
        },
        { enableHighAccuracy: true, timeout: 10000 },
      );
    });
  }

  /**
   * Asigna las coordenadas a los inputs del formulario
   */
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

  /**
   * Vincula el evento submit del formulario enviando los datos en ESPAÑOL al backend (routes.py)
   */
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

      // Construimos exactamente el payload con las claves y valores que exige schemas.py
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
          "Por favor, selecciona un punto en el mapa o usa el botón de geolocalización.",
        );
        return;
      }

      try {
        const response = await fetch("/api/necesidades", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payloadSpanish),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Error de validación del backend:", errorData);
          alert(
            `Error de validación: ${
              errorData.detalle || "Revisa los campos del formulario."
            }`,
          );
          return;
        }

        // La API devuelve la necesidad con su id, estado ("abierta") y creado_en
        const guardadaEnDB = await response.json();

        // Mapeo para la tarjeta/marcador local en el mapa
        const necesidadCreada = {
          id: guardadaEnDB.id,
          title: guardadaEnDB.titulo,
          type: guardadaEnDB.tipo,
          priority: guardadaEnDB.prioridad,
          description: guardadaEnDB.descripcion,
          latitude: guardadaEnDB.latitud,
          longitude: guardadaEnDB.longitud,
          status: guardadaEnDB.estado,
        };

        if (typeof this.onSubmit === "function") {
          this.onSubmit(necesidadCreada);
        }

        this.reset();
        alert("¡Necesidad registrada correctamente en la base de datos!");
      } catch (error) {
        console.error("Error de conexión:", error);
        alert("No se pudo conectar con el servidor.");
      }
    });
  }

  reset() {
    if (this.formElement) {
      this.formElement.reset();
    }
  }
}
