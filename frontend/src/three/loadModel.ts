import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { assetsApi } from "@/api";

export async function loadModelIntoScene(
  scene: THREE.Scene,
  camera: THREE.PerspectiveCamera,
  controls: any,
  modelId: number
) {
  // 1️⃣ Resolve real file URL
  const res = await assetsApi.getUrl(modelId);
  const url = res.data.url;

  console.log("Resolved GLB URL:", url);

  // 2️⃣ Load GLB
  const loader = new GLTFLoader();
  loader.setCrossOrigin("anonymous");

  loader.load(
    url,
    (gltf) => {
      console.log("GLB LOADED", gltf);

      const model = gltf.scene;

      // Clear old models
      scene.traverse((obj) => {
        if ((obj as any).isMesh) scene.remove(obj);
      });

      // Center
      const box = new THREE.Box3().setFromObject(model);
      const center = box.getCenter(new THREE.Vector3());
      model.position.sub(center);

      // Scale
      const size = box.getSize(new THREE.Vector3()).length();
      model.scale.setScalar(2 / size);

      scene.add(model);

      // Camera
      controls?.target.set(0, 0, 0);
      controls?.update();
      camera.lookAt(0, 0, 0);
    },
    undefined,
    (err) => {
      console.error("GLB LOAD FAILED", err);
    }
  );
}

