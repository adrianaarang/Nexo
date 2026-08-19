// frontend/js/core/mapa-necesidades/formularioNecesidad.js

export function inicializarFormulario(onSubmitCallback) {
  const form = document.getElementById('form-nueva-necesidad');
  if (!form) return;

  // Botón para autocompletar ubicación con GPS del dispositivo
  const btnGps = document.getElementById('btn-usar-gps');
  if (btnGps) {
    btnGps.addEventListener('click', () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            document.getElementById('input-lat').value = pos.coords.latitude;
            document.getElementById('input-lng').value = pos.coords.longitude;
          },
          (err) => console.warn('No se pudo obtener ubicación:', err)
        );
      }
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nuevaNecesidad = {
      titulo: form.querySelector('#input-titulo').value.trim(),
      tipo: form.querySelector('#select-tipo').value,
      prioridad: form.querySelector('#select-prioridad').value,
      descripcion: form.querySelector('#textarea-desc').value.trim(),
      latitud: parseFloat(form.querySelector('#input-lat').value),
      longitud: parseFloat(form.querySelector('#input-lng').value),
      estado: 'abierta'
    };

    if (!nuevaNecesidad.titulo || isNaN(nuevaNecesidad.latitud)) {
      alert('Por favor, completa los campos requeridos y marca la ubicación.');
      return;
    }

    await onSubmitCallback(nuevaNecesidad);
    form.reset();
  });
}