/**
 * Build a deterministic mesh path:
 * "Root/Child/Mesh"
 *
 * Stop at object group boundary: group name starts with "obj:"
 * Fallback for unnamed nodes: "unnamed-{indexWithinParent}"
 */
export function buildMeshPath(mesh) {
  if (!mesh) return null;

  const parts = [];
  let node = mesh;

  while (node) {
    // stop at object boundary group
    if (typeof node.name === "string" && node.name.startsWith("obj:")) break;

    const parent = node.parent;

    let name =
      node.name && String(node.name).trim()
        ? String(node.name).trim()
        : null;

    if (!name) {
      if (parent && Array.isArray(parent.children)) {
        const idx = parent.children.indexOf(node);
        name = `unnamed-${Math.max(0, idx)}`;
      } else {
        name = "unnamed-0";
      }
    }

    parts.push(name);
    node = parent;
  }

  parts.reverse();
  return parts.join("/");
}
