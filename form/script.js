function selectOption(value) {
  const tipos = document.querySelectorAll(".Tipo1, .Tipo2");

  tipos.forEach((tipo) => {
    tipo.classList.remove("active");
    tipo.style.border = "1px solid #E5E7EB";
    tipo.style.backgroundColor = "#FFFFFF";
    const texto = tipo.querySelector('[data-layer="text"] div');
    if (texto) {
      texto.style.color = "#1F2937";
    }
  });

  document.getElementById(value).checked = true;
  const selectedContainer = document
    .getElementById(value)
    .closest(`[data-layer="tipo-${value === "casa" ? "2" : "1"}"]`);

  selectedContainer.classList.add("active");
  selectedContainer.style.border = "2px solid #8DFF00";
  selectedContainer.style.backgroundColor = "#F9FFF2";
  const selectedText = selectedContainer.querySelector(
    '[data-layer="text"] div'
  );
  if (selectedText) {
    selectedText.style.color = "#7021EB";
  }
  sessionStorage.setItem("tipo_propiedad", value);
}

window.addEventListener("DOMContentLoaded", () => {
  const tipoGuardado = sessionStorage.getItem("tipo_propiedad");
  if (tipoGuardado === "departamento" || tipoGuardado === "casa") {
    selectOption(tipoGuardado);
  }

  // Restaurar archivos guardados
  const fotosGuardadas = JSON.parse(sessionStorage.getItem("fotos")) || [];
  fotosGuardadas.forEach((nombre) => {
    mostrarArchivo(nombre, "filesDrop", "fotos");
  });

  const archivosApoyo =
    JSON.parse(sessionStorage.getItem("archivos_apoyo")) || [];
  archivosApoyo.forEach((nombre) => {
    mostrarArchivo(nombre, "supportFilesDrop", "archivos_apoyo");
  });
});

function mostrarArchivo(nombre, contenedorId, tipoStorage) {
  const container = document.getElementById(contenedorId);

  // Evita mostrar archivos duplicados visualmente
  const yaExiste = Array.from(container.children).some((child) =>
    child.textContent.includes(nombre)
  );
  if (yaExiste) return;

  const fileContainer = document.createElement("div");
  fileContainer.className = "file-container";
  fileContainer.style.display = "flex";
  fileContainer.style.alignItems = "center";
  fileContainer.style.justifyContent = "space-between";
  fileContainer.style.marginTop = "1px";
  fileContainer.style.padding = "10px";
  fileContainer.style.borderRadius = "4px";
  fileContainer.style.backgroundColor = "#f8f9fa";

  const fileInfo = document.createElement("div");
  fileInfo.style.color = "#007bff";
  fileInfo.style.fontSize = "12px";
  fileInfo.style.fontWeight = "bold";
  const displayFileName =
    nombre.length > 30 ? nombre.substring(0, 30) + "..." : nombre;
  fileInfo.textContent = `Archivo: ${displayFileName}`;

  const deleteButton = document.createElement("button");
  deleteButton.textContent = "×";
  deleteButton.style.border = "none";
  deleteButton.style.background = "none";
  deleteButton.style.color = "#dc3545";
  deleteButton.style.fontSize = "16px";
  deleteButton.style.cursor = "pointer";
  deleteButton.style.marginLeft = "8px";
  deleteButton.style.padding = "0 4px";

  deleteButton.addEventListener("click", () => {
    fileContainer.remove();

    const archivos = JSON.parse(sessionStorage.getItem(tipoStorage)) || [];
    sessionStorage.setItem(
      tipoStorage,
      JSON.stringify(archivos.filter((f) => f !== nombre))
    );
  });
  fileContainer.appendChild(fileInfo);
  fileContainer.appendChild(deleteButton);
  container.appendChild(fileContainer);
}
