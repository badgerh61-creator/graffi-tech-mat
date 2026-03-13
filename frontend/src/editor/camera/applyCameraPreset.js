import * as THREE from "three";
import { presetDirection, frameSphereWithDirection } from "./cameraFrame";

export function applyCameraPreset({
  camera,
  controls,
  bounds,
  preset = "iso",
}) {
  if (!camera || !controls || !bounds || bounds.isEmpty()) return;

  const sphere = new THREE.Sphere();
  bounds.getBoundingSphere(sphere);

  const { position, target } = frameSphereWithDirection({
    center: sphere.center,
    radius: sphere.radius,
    direction: presetDirection(preset),
    fovDeg: camera.fov || 50,
    fitOffset: 1.35,
  });

  camera.position.copy(position);
  controls.target.copy(target);
  camera.updateProjectionMatrix();
  controls.update();
}
