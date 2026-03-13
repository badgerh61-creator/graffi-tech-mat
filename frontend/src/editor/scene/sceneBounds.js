import * as THREE from "three";

export function computeVisibleSceneBounds(root) {
  const box = new THREE.Box3();
  let found = false;

  if (!root) return box.makeEmpty();

  root.traverse((obj) => {
    if (!obj?.isMesh) return;
    if (obj.visible === false) return;

    if (!obj.geometry?.boundingBox) {
      obj.geometry?.computeBoundingBox?.();
    }

    const objBox = new THREE.Box3().setFromObject(obj);
    if (objBox.isEmpty()) return;

    if (!found) {
      box.copy(objBox);
      found = true;
    } else {
      box.union(objBox);
    }
  });

  return found ? box : box.makeEmpty();
}

export function computeSelectedBounds(root, selectedId) {
  const box = new THREE.Box3();
  if (!root || !selectedId) return box.makeEmpty();

  const sid = String(selectedId);
  const objectId = sid.split("::")[0];

  let found = false;

  root.traverse((obj) => {
    if (!obj) return;
    if (obj.userData?.objectId !== objectId) return;
    if (obj.visible === false) return;

    const objBox = new THREE.Box3().setFromObject(obj);
    if (objBox.isEmpty()) return;

    if (!found) {
      box.copy(objBox);
      found = true;
    } else {
      box.union(objBox);
    }
  });

  return found ? box : box.makeEmpty();
}
