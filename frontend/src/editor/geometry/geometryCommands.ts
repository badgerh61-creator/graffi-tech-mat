// frontend/src/editor/geometry/geometryCommands.ts

export type GeometryCommand =
  | {
      command: "TRANSLATE";
      target_id: string;
      delta: { x: number; y: number; z: number };
    }
  | {
      command: "ROTATE";
      target_id: string;
      axis: "x" | "y" | "z";
      degrees: number;
    }
  | {
      command: "SCALE";
      target_id: string;
      axis: "uniform" | "x" | "y" | "z";
      factor: number;
    };
