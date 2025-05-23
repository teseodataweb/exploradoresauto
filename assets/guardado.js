//contact.html
// Guardar datos y avanzar
document.getElementById("BtnAdelante").addEventListener("click", function (e) {
  e.preventDefault();
  const fields = [
    "nombre",
    "Dedication",
    "prefijo",
    "numerotelefono",
    "email",
    "empresa",
    "razon",
    "DescribeRazon",
  ];

  let valid = true;
  fields.forEach((id) => {
    const el = document.getElementById(id);
    if (!el || !el.value.trim()) {
      el.focus();
      valid = false;
    } else {
      sessionStorage.setItem(id, el.value);
    }
  });

  if (valid) {
    window.location.href = "/form/step1.html";
  }
});

// Restaurar datos al cargar
window.addEventListener("DOMContentLoaded", () => {
  const fields = [
    "nombre",
    "Dedication",
    "prefijo",
    "numerotelefono",
    "email",
    "empresa",
    "razon",
    "DescribeRazon",
  ];

  fields.forEach((id) => {
    const el = document.getElementById(id);
    const saved = sessionStorage.getItem(id);
    if (el && saved) {
      el.value = saved;
    }
  });
});
