import { EngineBridge } from "./EngineBridge";

const scene = {
  root: {
    id: "root",
    name: "Root",
    type: "group",
    transform: {
      position: [0, 0, 0],
      rotation: [0, 0, 0],
      scale: [1, 1, 1],
    },
    children: [
      {
        id: "cube-1",
        name: "Cube",
        type: "mesh",
        transform: {
          position: [0, 1, 0],
          rotation: [0, 0, 0],
          scale: [1, 1, 1],
        },
        children: [],
      },
    ],
  },
};

EngineBridge.createScene(scene);
const saved = EngineBridge.serialize();
EngineBridge.load(saved);

console.log("Serialized:", saved);
console.log("Reloaded:", EngineBridge.getScene());

