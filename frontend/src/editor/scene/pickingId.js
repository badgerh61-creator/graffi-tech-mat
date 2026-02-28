import { buildMeshPath } from "./meshPath";

/**
 * Canonical picked ID:
 *   "{objectKey}::{meshPath}"
 * where objectKey is either:
 *   - "{objectId}"
 *   - "{objectId}@{instanceId}"
 */
export function buildPickedTargetId({ objectKey, objectId, mesh }) {
  const key = objectKey || objectId;
  if (!key || !mesh) return null;

  const meshPath = buildMeshPath(mesh);
  if (!meshPath) return null;

  return `${key}::${meshPath}`;
}
