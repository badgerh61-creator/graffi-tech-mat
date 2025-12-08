// src/utils/fileClassifier.js

export function classifyFile(file) {
  const name = file.name.toLowerCase();

  if (name.endsWith(".glb") || name.endsWith(".gltf"))
    return "model";

  if (
    name.endsWith(".png") ||
    name.endsWith(".jpg") ||
    name.endsWith(".jpeg") ||
    name.endsWith(".webp") ||
    name.endsWith(".bmp") ||
    name.endsWith(".gif") ||
    name.endsWith(".tiff") ||
    name.endsWith(".svg")
  ) return "image";

  if (name.endsWith(".hdr") || name.endsWith(".exr"))
    return "hdri";

  return "asset"; // fallback for anything else
}
