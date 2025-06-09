//contact.html
// Guardar datos y avanzar
document.getElementById("BtnAdelante").addEventListener("click", function (e) {
  e.preventDefault();

  // IDs de los campos a validar
  const fields = [
    "nombre",
    "Dedication",
    "prefijo",
    "numerotelefono",
    "email",
    "razon"
  ];

  let valid = true;
  let firstInvalidEl = null;

  // 1) Validar "nombre": solo letras, espacios, acentos, entre 3 y 50 caracteres
  const nombreEl = document.getElementById("nombre");
  const nombreRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]{3,50}$/;
  if (!nombreEl.value.trim() || !nombreRegex.test(nombreEl.value.trim())) {
    setErrorMessage(nombreEl, "Campo obligatorio: solo letras");
    if (!firstInvalidEl) firstInvalidEl = nombreEl;
    valid = false;
  } else {
    setErrorMessage(nombreEl, "");
    sessionStorage.setItem("nombre", nombreEl.value.trim());
  }

  // 2) Validar "Dedication" (select): no debe ser vacío
  const dedEl = document.getElementById("Dedication");
  if (dedEl.value === "") {
    setErrorMessage(dedEl, "Campo obligatorio");
    if (!firstInvalidEl) firstInvalidEl = dedEl;
    valid = false;
  } else {
    setErrorMessage(dedEl, "");
    dedEl.style.border = "";
    sessionStorage.setItem("Dedication", dedEl.value);
  }

  // 3) Validar "prefijo": exactamente 2 dígitos numéricos
  const prefEl = document.getElementById("prefijo");
  if (prefEl.value.length !== 2) {
    prefEl.classList.add("input-error");
    if (!firstInvalidEl) firstInvalidEl = prefEl;
    valid = false;
  } else {
    prefEl.classList.remove("input-error");
    sessionStorage.setItem("prefijo", prefEl.value);
  }

  // 4) Validar "numerotelefono": exactamente 10 dígitos numéricos
  const numTelEl = document.getElementById("numerotelefono");
  if (numTelEl.value.length !== 10) {
    numTelEl.classList.add("input-error");
    if (!firstInvalidEl) firstInvalidEl = numTelEl;
    valid = false;
  } else {
    numTelEl.classList.remove("input-error");
    sessionStorage.setItem("numerotelefono", numTelEl.value);
  }

  // 5) Validar "email": formato válido
  const emailEl = document.getElementById("email");
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailEl.value.trim() || !emailRegex.test(emailEl.value.trim())) {
    setErrorMessage(emailEl, "Ingrese un correo electrónico válido");
    if (!firstInvalidEl) firstInvalidEl = emailEl;
    valid = false;
  } else {
    setErrorMessage(emailEl, "");
    sessionStorage.setItem("email", emailEl.value.trim());
  }

  // 6) Validar "razon": no puede estar vacío
  const razonEl = document.getElementById("razon");
  if (!razonEl.value.trim()) {
    setErrorMessage(razonEl, "Campo obligatorio");
    if (!firstInvalidEl) firstInvalidEl = razonEl;
    valid = false;
  } else {
    setErrorMessage(razonEl, "");
    sessionStorage.setItem("razon", razonEl.value.trim());
  }

  // Guardar empresa y DescribeRazon sin validación
  const empresaEl = document.getElementById("empresa");
  if (empresaEl) {
    sessionStorage.setItem("empresa", empresaEl.value.trim());
  }

  const describeEl = document.getElementById("DescribeRazon");
  if (describeEl) {
    sessionStorage.setItem("DescribeRazon", describeEl.value.trim());
  }

  // Si hay algún campo inválido, enfocar el primero y no avanzar
  if (!valid) {
    firstInvalidEl.focus();
    return;
  }

  // Si todos son válidos, redirigir al step1.html
  window.location.href = "../form/step1.html";
});

// Función setErrorMessage (si no la tienes definida en otro script)
function setErrorMessage(inputElement, message) {
  let errorSpan = inputElement.nextElementSibling;
  // Si no existe un <span> de error, crearlo
  if (!errorSpan || !errorSpan.classList.contains("error-msg")) {
    errorSpan = document.createElement("span");
    errorSpan.classList.add("error-msg");
    inputElement.parentNode.insertBefore(errorSpan, inputElement.nextSibling);
  }
  // Mostrar u ocultar mensaje
  if (message) {
    errorSpan.textContent = message;
    errorSpan.style.color = "red";
    errorSpan.style.fontFamily = "DM Sans";
    errorSpan.style.fontSize = "0.785rem";
    errorSpan.style.marginTop = "2px";
    errorSpan.style.letterSpacing = "1px";
    errorSpan.style.display = "block";
  } else {
    errorSpan.textContent = "";
    errorSpan.style.display = "none";
  }
}

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
