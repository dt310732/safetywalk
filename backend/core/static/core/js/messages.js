document.addEventListener("DOMContentLoaded", () => {
  if (!window.djangoMessages || !window.djangoMessages.length) return;
  const container = document.getElementById("toast-container");
  if (!container) return;

  window.djangoMessages.forEach((msg) => {
    const toast = document.createElement("div");

    let type = "info";
    if (msg.level.includes("error")) type = "error";
    if (msg.level.includes("success")) type = "success";

    toast.className = `toast ${type}`;
    toast.textContent = msg.text;

    container.appendChild(toast);

    setTimeout(() => toast.remove(), 3500);
  });

  // zabezpieczenie przed podwójnym wyświetleniem
  window.djangoMessages = [];
});
