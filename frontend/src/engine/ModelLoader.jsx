import React, { useMemo } from "react";
import { useGLTF } from "@react-three/drei";
import * as THREE from "three";

/* ================= INTERNAL GLTF MODEL ================= */
function GLTFModel({ url }) {
  // ❗ useGLTF MUST be unconditional
  const gltf = useGLTF(url);

  const scene = useMemo(() => {
    if (!gltf || !gltf.scene) return null;

    const root = gltf.scene.clone(true);

    // Center + normalize
    const box = new THREE.Box3().setFromObject(root);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());

    root.position.sub(center);
    root.position.y += size.y / 2;

    const maxDim = Math.max(size.x, size.y, size.z) || 1;
    root.scale.setScalar(1.5 / maxDim);

    return root;
  }, [gltf]);

  if (!scene) return null;
  return <primitive object={scene} />;
}

/* ================= PUBLIC WRAPPER ================= */
export default function ModelLoader({ url }) {
  // ✅ HARD GUARDS (NO INVALID URL EVER)
  if (!url || typeof url !== "string") return null;
  if (!url.startsWith("http")) return null;

  return <GLTFModel url={url} />;
}
