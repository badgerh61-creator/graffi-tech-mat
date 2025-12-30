import { SceneGraph } from "../../../engine/scene/SceneGraph";
import { EngineBridge } from "./EngineBridge";

export function loadScene(scene: SceneGraph) {
  EngineBridge.createScene(scene);
}

export function saveScene(): string {
  return EngineBridge.serialize();
}

