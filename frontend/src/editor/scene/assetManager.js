const activeLoads = new Map();

export function beginLoad(objectId) {
  const id = String(objectId);
  const requestId = Symbol("load");

  activeLoads.set(id, requestId);

  return requestId;
}

export function isLoadValid(objectId, requestId) {
  return activeLoads.get(String(objectId)) === requestId;
}

export function clearLoad(objectId) {
  activeLoads.delete(String(objectId));
}

export function clearAllLoads() {
  activeLoads.clear();
}
