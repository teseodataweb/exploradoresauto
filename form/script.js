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
}

//Subir Archivos
function handlePhotoSelect(file, fileInput) {
  const filesContainer = document.getElementById("filesDrop");
  const existingFiles = filesContainer.querySelectorAll(".file-container");

  if (existingFiles.length >= 100) {
    alert("Solo se pueden subir hasta 100 fotografías");
    fileInput.value = "";
    return;
  }

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
  const fileName =
    file.name.length > 30 ? file.name.substring(0, 30) + "..." : file.name;
  fileInfo.textContent = `Archivo: ${fileName}`;

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
    fileInput.value = "";
    fileContainer.remove();
  });

  fileContainer.appendChild(fileInfo);
  fileContainer.appendChild(deleteButton);
  filesContainer.appendChild(fileContainer);
}

// Función para manejar la selección de archivos de información
function handleSupportFilesSelect(file, fileInput) {
  const supportFilesContainer = document.getElementById("supportFilesDrop");
  const existingFiles =
    supportFilesContainer.querySelectorAll(".file-container");

  const fileName = file.name;
  const existingFileNames = Array.from(existingFiles).map(
    (container) => container.querySelector("div").textContent.split(": ")[1]
  );

  if (existingFileNames.includes(fileName)) {
    alert("Este archivo ya ha sido agregado");
    fileInput.value = "";
    return;
  }

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
    fileName.length > 30 ? fileName.substring(0, 30) + "..." : fileName;
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
    fileInput.value = "";
    fileContainer.remove();
  });

  fileContainer.appendChild(fileInfo);
  fileContainer.appendChild(deleteButton);
  supportFilesContainer.appendChild(fileContainer);
}

// Al clicar en "examinar" de foto, abre selector
document
  .getElementById("fotoLink")
  .addEventListener("click", () =>
    document.getElementById("fotoInput").click()
  );

// Agregar evento para mostrar el nombre del archivo seleccionado
document.getElementById("fotoInput").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    handlePhotoSelect(file, e.target);
  }
});

// Al clicar en "examinar" de archivos de apoyo, abre selector
document
  .getElementById("filesLink")
  .addEventListener("click", () =>
    document.getElementById("filesInput").click()
  );

// Agregar evento para mostrar el nombre del archivo seleccionado
document.getElementById("filesInput").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    handleSupportFilesSelect(file, e.target);
  }
});

// Manejar el arrastrar y soltar archivos para la foto
const dropArea = document.getElementById("filesDrop");
dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.style.border = "none";
});

dropArea.addEventListener("dragleave", () => {
  dropArea.style.border = "none";
});

dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.style.border = "none";
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    const fileInput = document.getElementById("fotoInput");
    fileInput.files = files;
    handlePhotoSelect(files[0], fileInput);
  }
});

// Manejar el arrastrar y soltar archivos para la información de apoyo
const supportDropArea = document.getElementById("supportFilesDrop");
supportDropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  supportDropArea.style.border = "none";
});

supportDropArea.addEventListener("dragleave", () => {
  supportDropArea.style.border = "none";
});

supportDropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  supportDropArea.style.border = "none";
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    const fileInput = document.getElementById("filesInput");
    fileInput.files = files;
    handleSupportFilesSelect(files[0], fileInput);
  }
});
