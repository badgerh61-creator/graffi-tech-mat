// src/engine/ModelLoader.jsx
import React from "react"
import { useGLTF } from "@react-three/drei"

export default function ModelLoader({ url }) {
  const gltf = useGLTF(url, true);
  return <primitive object={gltf.scene} />;
}
