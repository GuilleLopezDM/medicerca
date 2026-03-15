// TODO (Diego) — JavaScript personalizado
// Podés agregar interactividad acá si la necesitás.

// Ejemplo: auto-cerrar flash messages después de 4 segundos
document.addEventListener("DOMContentLoaded", () => {
  const alertas = document.querySelectorAll("[data-flash]");
  alertas.forEach(alerta => {
    setTimeout(() => {
      alerta.style.transition = "opacity 0.5s";
      alerta.style.opacity = "0";
      setTimeout(() => alerta.remove(), 500);
    }, 4000);
  });
});
