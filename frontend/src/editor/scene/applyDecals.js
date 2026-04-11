import * as THREE from "three";
import { DecalGeometry } from "three/examples/jsm/geometries/DecalGeometry.js";

/**
 * Tier 6G.15 — Apply decals onto mesh
 */
export async function applyDecals(group, decalState = []) {
  if (!group || !decalState || !decalState.length) return;

  // 🔥 Properly remove old decals (SAFE)
  const toRemove = [];

  group.children.forEach((child) => {
    if (child.name?.startsWith("decal:")) {
      toRemove.push(child);
    }
  });

  toRemove.forEach((child) => {
    group.remove(child);

    if (child.geometry) child.geometry.dispose();

    if (child.material) {
      if (child.material.map) child.material.map.dispose();
      child.material.dispose();
    }
  });

  // collect meshes
  const meshes = [];
  group.traverse((node) => {
    if (node.isMesh) meshes.push(node);
  });

  if (!meshes.length) return;

  const targetMesh = meshes[0]; // simple version

  for (const decal of decalState) {
    try {
      const texture = await new THREE.TextureLoader().loadAsync(
        decal.texture_url
      );

      texture.encoding = THREE.sRGBEncoding;

      const material = new THREE.MeshStandardMaterial({
        map: texture,
        transparent: true,
        depthWrite: false,
        polygonOffset: true,
        polygonOffsetFactor: -4,
      });

      const position = new THREE.Vector3(
        decal.position?.x || 0,
        decal.position?.y || 0,
        decal.position?.z || 0
      );

      const rotation = new THREE.Euler(
        decal.rotation?.x || 0,
        decal.rotation?.y || 0,
        decal.rotation?.z || 0
      );

      const scale = new THREE.Vector3(
        decal.scale?.x || 1,
        decal.scale?.y || 1,
        decal.scale?.z || 1
      );

      const geometry = new DecalGeometry(
        targetMesh,
        position,
        rotation,
        scale
      );

      const decalMesh = new THREE.Mesh(geometry, material);
      decalMesh.name = `decal:${decal.id}`;

      group.add(decalMesh);

    } catch (err) {
      console.error("❌ Decal failed:", err);
    }
  }
}
