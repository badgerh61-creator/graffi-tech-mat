export function buildPickedTargetId({ objectId, mesh }) {
  const meshKey = (mesh?.name && String(mesh.name).trim()) ? mesh.name : mesh?.uuid;
  if (!objectId || !meshKey) return null;
  return `${objectId}::${meshKey}`;
}
