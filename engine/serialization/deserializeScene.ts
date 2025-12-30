import { SceneGraph } from "../scene/SceneGraph";

export function deserializeScene(raw: string): SceneGraph {
  return JSON.parse(raw);
}

