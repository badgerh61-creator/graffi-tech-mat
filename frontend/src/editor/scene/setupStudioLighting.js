import * as THREE from "three";
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

export async function setupStudioLighting({
  renderer,
  scene,
  hdrUrl,
  exposure = 1.0,
  envIntensity = 1.0,
}) {
  // renderer settings (deterministic)
  renderer.physicallyCorrectLights = true;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = exposure;

  // remove existing studio lights (if re-run)
  const toRemove = [];
  scene.traverse((o) => {
    if (o.userData && o.userData.__studioLight) toRemove.push(o);
  });
  toRemove.forEach((o) => o.parent && o.parent.remove(o));

  // 3-point lighting (fallback even if HDR fails)
  const key = new THREE.DirectionalLight(0xffffff, 2.5);
  key.position.set(5, 6, 3);
  key.userData.__studioLight = true;

  const fill = new THREE.DirectionalLight(0xffffff, 1.2);
  fill.position.set(-6, 3, 4);
  fill.userData.__studioLight = true;

  const rim = new THREE.DirectionalLight(0xffffff, 1.6);
  rim.position.set(-2, 5, -6);
  rim.userData.__studioLight = true;

  const amb = new THREE.AmbientLight(0xffffff, 0.2);
  amb.userData.__studioLight = true;

  scene.add(key, fill, rim, amb);

  // Environment (HDR)
  const pmrem = new THREE.PMREMGenerator(renderer);
  pmrem.compileEquirectangularShader();

  const loader = new RGBELoader();
  try {
    const hdr = await loader.loadAsync(hdrUrl);
    hdr.mapping = THREE.EquirectangularReflectionMapping;

    const env = pmrem.fromEquirectangular(hdr).texture;
    scene.environment = env;
    scene.background = null; // studio black background, or set to env if you want
    hdr.dispose();
  } catch (e) {
    // fallback: no env
    scene.environment = null;
  } finally {
    pmrem.dispose();
  }

  // apply envIntensity to meshes (optional)
  // easiest deterministic approach: set material.envMapIntensity
  scene.traverse((o) => {
    if (!o.isMesh) return;
    const m = o.material;
    if (m && typeof m === "object") {
      if ("envMapIntensity" in m) m.envMapIntensity = envIntensity;
      m.needsUpdate = true;
    }
  });
}
