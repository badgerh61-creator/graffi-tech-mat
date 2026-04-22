import * as THREE from "three";
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

export async function setupStudioLighting({
  renderer,
  scene,
  hdrUrl,
  exposure = 1.2,
  envIntensity = 1.3,
}) {
  // -----------------------
  // Renderer config
  // -----------------------
  renderer.useLegacyLights = false;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = exposure;

  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  // -----------------------
  // Remove previous studio lights
  // -----------------------
  const toRemove = [];
  scene.traverse((o) => {
    if (o.userData?.__studioLight) toRemove.push(o);
  });
  toRemove.forEach((o) => o.parent?.remove(o));

  // -----------------------
  // HDR ENVIRONMENT
  // -----------------------
  const pmrem = new THREE.PMREMGenerator(renderer);
  pmrem.compileEquirectangularShader();

  const loader = new RGBELoader();

  let hdrLoaded = false;

  try {
    const hdr = await loader.loadAsync(hdrUrl);
    hdr.mapping = THREE.EquirectangularReflectionMapping;

    const env = pmrem.fromEquirectangular(hdr).texture;

    scene.environment = env;

    // ✅ FIX: show HDR for proper visual lighting
    scene.background = env;

    hdr.dispose();
    hdrLoaded = true;

  } catch (e) {
    console.warn("HDR failed, using fallback lighting");
    scene.environment = null;
    scene.background = null;
  } finally {
    pmrem.dispose();
  }

  // -----------------------
  // LIGHTING LOGIC
  // -----------------------

  if (hdrLoaded) {
    const soft = new THREE.DirectionalLight(0xffffff, 0.6);
    soft.position.set(5, 10, 5);

    // ✅ CRITICAL — enable shadows
    soft.castShadow = true;

    // ✅ SHADOW QUALITY SETTINGS
    soft.shadow.mapSize.width = 1024;
    soft.shadow.mapSize.height = 1024;

    soft.shadow.camera.near = 0.5;
    soft.shadow.camera.far = 50;

    soft.shadow.camera.left = -10;
    soft.shadow.camera.right = 10;
    soft.shadow.camera.top = 10;
    soft.shadow.camera.bottom = -10;

    soft.userData.__studioLight = true;
    scene.add(soft);

  } else {
    // Fallback lighting (only if HDR fails)

    const key = new THREE.DirectionalLight(0xffffff, 2.0);
    key.position.set(5, 6, 3);
    key.castShadow = true;
    key.userData.__studioLight = true;

    const fill = new THREE.DirectionalLight(0xffffff, 1.0);
    fill.position.set(-6, 3, 4);
    fill.userData.__studioLight = true;

    const rim = new THREE.DirectionalLight(0xffffff, 1.2);
    rim.position.set(-2, 5, -6);
    rim.userData.__studioLight = true;

    const amb = new THREE.AmbientLight(0xffffff, 0.2);
    amb.userData.__studioLight = true;

    scene.add(key, fill, rim, amb);
  }

  // -----------------------
  // Apply env intensity
  // -----------------------
  scene.traverse((o) => {
    if (!o.isMesh) return;

    const mats = Array.isArray(o.material)
      ? o.material
      : [o.material];

    mats.forEach((mat) => {
      if (!mat) return;

      if ("envMapIntensity" in mat) {
        mat.envMapIntensity = envIntensity;
      }

      mat.needsUpdate = true;
    });
  });
}
