// Slider moderno de la base común: autoplay con barra de progreso,
// flechas, puntos clicables y soporte de gesto táctil (swipe).
// Uso: cualquier página con la estructura .nexo-slider > .nexo-slider__track
// puede llamar a iniciarSlider(document.querySelector(".nexo-slider")).

export function iniciarSlider(root, { intervalo = 6000 } = {}) {
  if (!root) return;
  const track = root.querySelector(".nexo-slider__track");
  const slides = Array.from(track.children);
  const dotsWrap = root.querySelector(".nexo-slider__dots");
  const prevBtn = root.querySelector("[data-slider-prev]");
  const nextBtn = root.querySelector("[data-slider-next]");

  let actual = 0;
  let timer = null;

  // puntos de progreso
  const dots = slides.map((_, i) => {
    const dot = document.createElement("button");
    dot.className = "nexo-slider__dot";
    dot.setAttribute("aria-label", `Ir a la diapositiva ${i + 1}`);
    dot.innerHTML = '<span class="fill"></span>';
    dot.addEventListener("click", () => irA(i));
    dotsWrap.appendChild(dot);
    return dot;
  });

  function pintar() {
    track.style.transform = `translateX(-${actual * 100}%)`;
    dots.forEach((dot, i) => {
      dot.classList.toggle("done", i < actual);
      dot.classList.remove("active");
      if (i === actual) {
        // reinicia la animación de progreso
        void dot.offsetWidth;
        dot.classList.add("active");
      }
    });
  }

  function irA(i) {
    actual = (i + slides.length) % slides.length;
    pintar();
    reiniciarAutoplay();
  }

  function reiniciarAutoplay() {
    clearInterval(timer);
    timer = setInterval(() => irA(actual + 1), intervalo);
  }

  prevBtn?.addEventListener("click", () => irA(actual - 1));
  nextBtn?.addEventListener("click", () => irA(actual + 1));

  // pausa al pasar el ratón
  root.addEventListener("mouseenter", () => clearInterval(timer));
  root.addEventListener("mouseleave", reiniciarAutoplay);

  // swipe táctil
  let touchX = null;
  root.addEventListener("touchstart", (e) => (touchX = e.touches[0].clientX), { passive: true });
  root.addEventListener(
    "touchend",
    (e) => {
      if (touchX === null) return;
      const delta = e.changedTouches[0].clientX - touchX;
      if (Math.abs(delta) > 40) irA(actual + (delta < 0 ? 1 : -1));
      touchX = null;
    },
    { passive: true }
  );

  pintar();
  reiniciarAutoplay();
}
