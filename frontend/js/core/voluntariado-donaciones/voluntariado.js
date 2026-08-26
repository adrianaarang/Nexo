import { el } from '../../shared/utils.js';
import { createVolunteer, getVolunteers, updateVolunteerStatus } from './voluntariadoApi.js';

const volunteersList = document.querySelector('[data-volunteers-list]');
const volunteersEmpty = document.querySelector('[data-volunteers-empty]');
const statusFilter = document.querySelector('[data-status-filter]');
const formPanel = document.querySelector('[data-volunteer-form-panel]');
const volunteerForm = document.getElementById('volunteer-form');
const formStatus = document.querySelector('[data-form-status]');
const calendar = document.querySelector('[data-availability-calendar]');
const vehicleType = document.querySelector('[data-vehicle-type]');
const vehicleTypeSelect = volunteerForm.elements.vehicle_type;
const dniInput = volunteerForm.elements.dni;
const taskInputs = [...volunteerForm.querySelectorAll('input[name="tasks"]')];

const STATUS_LABELS = { available: 'Disponible', assigned: 'Asignado a tarea', resting: 'No disponible / descansando' };
const REQUIRED_MESSAGES = {
  first_name: 'El nombre es un campo necesario para enviar el formulario.',
  last_name: 'Los apellidos son un campo necesario para enviar el formulario.',
  dni: 'El DNI es un campo necesario para enviar el formulario.',
  phone: 'El teléfono es un campo necesario para enviar el formulario.',
  birth_date: 'La fecha de nacimiento es un campo necesario para enviar el formulario.',
  locality: 'La localidad donde puedes ayudar es un campo necesario para enviar el formulario.',
};
const DNI_LETTERS = 'TRWAGMYFPDXBNJZSQVHLCKE';

function setFormVisible(isVisible) {
  formPanel.hidden = !isVisible;
  if (isVisible) volunteerForm.elements.first_name.focus();
}

function formatLocalDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function renderAvailabilityCalendar() {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const days = Array.from({ length: 7 }, (_, index) => {
    const date = new Date(today);
    date.setDate(today.getDate() + index);
    return date;
  });

  calendar.replaceChildren(el('span', { class: 'nexo-voluntarios__calendar-header', text: 'Hora' }));
  days.forEach((date) => calendar.append(el('span', {
    class: 'nexo-voluntarios__calendar-header',
    text: new Intl.DateTimeFormat('es-ES', { weekday: 'short', day: 'numeric' }).format(date),
  })));
  for (let hour = 0; hour < 24; hour += 1) {
    calendar.append(el('span', { class: 'nexo-voluntarios__calendar-hour', text: `${String(hour).padStart(2, '0')}:00` }));
    days.forEach((date) => {
      const dateValue = formatLocalDate(date);
      const hourValue = String(hour).padStart(2, '0');
      const input = el('input', { type: 'checkbox', name: 'availability_slots', value: `${dateValue}T${hourValue}:00:00` });
      calendar.append(el('label', {
        class: 'nexo-voluntarios__calendar-slot',
        'aria-label': `Disponible el ${dateValue} a las ${hourValue}:00`,
      }, [input]));
    });
  }
}

function getAvailabilitySlots(formData) {
  return formData.getAll('availability_slots').map((slot) => ({ starts_at: slot }));
}

function updateVehicleTypeVisibility() {
  const hasOwnVehicle = volunteerForm.elements.transportation.value === 'own_vehicle';
  vehicleType.hidden = !hasOwnVehicle;
  vehicleTypeSelect.disabled = !hasOwnVehicle;
  vehicleTypeSelect.required = hasOwnVehicle;
  if (!hasOwnVehicle) vehicleTypeSelect.value = '';
}

function validateDni() {
  const dni = dniInput.value.toUpperCase();
  dniInput.value = dni;
  if (!dni) {
    dniInput.setCustomValidity('');
    return;
  }
  if (!/^\d{8}[A-Z]$/.test(dni)) {
    dniInput.setCustomValidity('Introduce 8 números y una letra, sin espacios.');
    return;
  }
  const expectedLetter = DNI_LETTERS[Number(dni.slice(0, 8)) % 23];
  dniInput.setCustomValidity(dni.at(-1) === expectedLetter ? '' : 'El DNI no es válido: la letra de control no coincide.');
}

function validateTasks() {
  const hasTask = taskInputs.some((input) => input.checked);
  if (!hasTask) {
    formStatus.textContent = 'Selecciona al menos una tarea para enviar el formulario.';
    taskInputs[0].focus();
  }
  return hasTask;
}

function renderVolunteers(volunteers) {
  volunteersList.replaceChildren();
  volunteersEmpty.hidden = volunteers.length > 0;
  volunteers.forEach((volunteer) => {
    const status = volunteer.status || 'available';
    const fullName = volunteer.full_name || `${volunteer.first_name || ''} ${volunteer.last_name || ''}`.trim();
    const card = el('article', { class: 'nexo-card nexo-voluntarios__card' });
    const header = el('div', { class: 'nexo-voluntarios__card-header' }, [
      el('h3', { text: fullName }),
      el('span', { class: `nexo-badge nexo-voluntarios__status--${status}`, text: STATUS_LABELS[status] }),
    ]);
    const taskText = volunteer.tasks?.length ? volunteer.tasks.join(', ') : 'Sin tareas indicadas';
    const details = el('p', { text: taskText });
    const slotCount = volunteer.availability_slots?.length || 0;
    const locality = volunteer.locality || volunteer.location;
    const meta = el('p', { class: 'nexo-voluntarios__meta', text: `${locality} · ${slotCount} horas indicadas` });
    const statusSelect = el('select', { 'aria-label': `Actualizar estado de ${fullName}` });
    Object.entries(STATUS_LABELS).forEach(([value, label]) => statusSelect.add(new Option(label, value, false, value === status)));
    statusSelect.addEventListener('change', async () => {
      statusSelect.disabled = true;
      try {
        await updateVolunteerStatus(volunteer.id, statusSelect.value);
        renderVolunteers(await getVolunteers({ status: statusFilter.value }));
      } catch (error) {
        window.alert(error.message);
      } finally {
        statusSelect.disabled = false;
      }
    });
    card.append(header, details, meta, el('div', { class: 'nexo-voluntarios__card-footer' }, [statusSelect]));
    volunteersList.append(card);
  });
}

async function loadVolunteers() {
  volunteersList.textContent = 'Cargando voluntariado…';
  try {
    renderVolunteers(await getVolunteers({ status: statusFilter.value }));
  } catch (error) {
    volunteersList.textContent = error.message;
    volunteersEmpty.hidden = true;
  }
}

document.addEventListener('click', (event) => {
  if (event.target.closest('[data-action="show-form"]')) setFormVisible(true);
  if (event.target.closest('[data-action="hide-form"]')) setFormVisible(false);
});
statusFilter.addEventListener('change', loadVolunteers);
volunteerForm.elements.transportation.forEach((input) => input.addEventListener('change', updateVehicleTypeVisibility));
Object.entries(REQUIRED_MESSAGES).forEach(([fieldName, message]) => {
  const field = volunteerForm.elements[fieldName];
  field.addEventListener('invalid', () => {
    if (field.validity.valueMissing) field.setCustomValidity(message);
    else if (fieldName === 'first_name' || fieldName === 'last_name') field.setCustomValidity('Introduce un nombre válido; se admiten letras, espacios y signos de puntuación.');
  });
  field.addEventListener('input', () => field.setCustomValidity(''));
});
dniInput.addEventListener('input', validateDni);
volunteerForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!validateTasks()) return;
  const submitButton = volunteerForm.querySelector('[type="submit"]');
  const formData = new FormData(volunteerForm);
  submitButton.disabled = true;
  formStatus.textContent = 'Enviando…';
  try {
    await createVolunteer({
      first_name: formData.get('first_name'),
      last_name: formData.get('last_name'),
      dni: formData.get('dni').toUpperCase(),
      birth_date: formData.get('birth_date'),
      phone: formData.get('phone'),
      locality: formData.get('locality'),
      tasks: formData.getAll('tasks'),
      certifications: formData.getAll('certifications'),
      transportation: formData.get('transportation'),
      vehicle_type: formData.get('vehicle_type') || null,
      availability_slots: getAvailabilitySlots(formData),
      skills: formData.get('skills'),
    });
    volunteerForm.reset();
    updateVehicleTypeVisibility();
    formStatus.textContent = 'Solicitud enviada. Un administrador la revisará antes de publicarla.';
  } catch (error) {
    formStatus.textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
});

renderAvailabilityCalendar();
updateVehicleTypeVisibility();
loadVolunteers();
