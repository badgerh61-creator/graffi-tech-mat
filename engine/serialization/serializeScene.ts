import { SceneGraph } from "../scene/SceneGraph";

export function serializeScene(scene: SceneGraph): string {
  return JSON.stringify(scene);
}

