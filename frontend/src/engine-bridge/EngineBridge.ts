import { SceneGraph } from "../../../engine/scene/SceneGraph";
import { serializeScene } from "../../../engine/serialization/serializeScene";
import { deserializeScene } from "../../../engine/serialization/deserializeScene";

let currentScene: SceneGraph | null = null;

export const EngineBridge = {
  createScene(scene: SceneGraph) {
    currentScene = scene;
  },

  getScene(): SceneGraph | null {
    return currentScene;
  },

  serialize(): string {
    if (!currentScene) {
      throw new Error("No scene loaded");
    }
    return serializeScene(currentScene);
  },

  load(serialized: string) {
    currentScene = deserializeScene(serialized);
  },
};

