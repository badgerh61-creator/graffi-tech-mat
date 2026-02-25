import { buildMeshPath } from "./meshPath";

export function buildPickedTargetId({ objectId, mesh }) {
  if (!objectId || !mesh) return null;

  const meshPath = buildMeshPath(mesh);
  if (!meshPath) return null;

  return `${objectId}::${meshPath}`;
}
