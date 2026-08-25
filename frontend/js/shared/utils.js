// Funciones reutilizables — parte de la base común.
export function formatDate(isoString) {
  if (!isoString) return "";
  const date = new Date(isoString.replace(" ", "T"));
  if (Number.isNaN(date.getTime())) return isoString;
  return date.toLocaleString("es-ES", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([key, value]) => {
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else node.setAttribute(key, value);
  });
  children.forEach((child) => node.appendChild(child));
  return node;
}
