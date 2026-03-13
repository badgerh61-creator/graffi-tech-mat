function sortById(items) {
  return [...items].sort((a, b) => String(a?.id || "").localeCompare(String(b?.id || "")));
}

export function buildOutlinerTree(objects = []) {
  const nodes = new Map();
  const roots = [];

  for (const obj of sortById(objects || [])) {
    nodes.set(String(obj.id), { ...obj, children: [] });
  }

  for (const node of nodes.values()) {
    const pid = node.parent_id ? String(node.parent_id) : null;
    if (pid && nodes.has(pid)) {
      nodes.get(pid).children.push(node);
    } else {
      roots.push(node);
    }
  }

  for (const node of nodes.values()) {
    node.children = sortById(node.children);
  }

  return sortById(roots);
}
