// src/engine/dragDropHandlers.js
// Lightweight drag/drop helpers for Studio canvas

export function processFile(file) {
  if (!file) return null;
  const url = URL.createObjectURL(file);
  const id =
    (typeof crypto !== "undefined" && crypto.randomUUID && crypto.randomUUID()) ||
    `${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
  const name = file.name;
  const lower = name.toLowerCase();
  let type = "file";
  if (lower.endsWith(".glb") || lower.endsWith(".gltf") || lower.endsWith(".fbx") || lower.endsWith(".obj") || lower.endsWith(".usdz")) type = "model";
  if (/\.(png|jpe?g|webp|hdr|exr)$/i.test(lower)) type = "texture";
  return { id, name, url, size: file.size, file, type };
}

export function attachDropHandlers(element, { onAdd } = {}) {
  if (!element) return () => {};
  const onDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "copy";
    element.classList?.add?.("droppable");
  };
  const onDragLeave = (e) => {
    element.classList?.remove?.("droppable");
  };
  const onDrop = (e) => {
    e.preventDefault();
    element.classList?.remove?.("droppable");
    const files = Array.from(e.dataTransfer.files || []);
    if (!files.length) return;
    for (const file of files) {
      const asset = processFile(file);
      if (onAdd && typeof onAdd === "function") onAdd(asset);
    }
  };
  element.addEventListener("dragover", onDragOver);
  element.addEventListener("dragleave", onDragLeave);
  element.addEventListener("drop", onDrop);

  return () => {
    element.removeEventListener("dragover", onDragOver);
    element.removeEventListener("dragleave", onDragLeave);
    element.removeEventListener("drop", onDrop);
  };
}
