// frontend/src/editor/geometry/geometryBridge.ts

import { executeTool } from "../../services/studio/toolExecutionAdapter";
import type { GeometryCommand } from "./geometryCommands";

export async function applyGeometryCommand(args: {
  snapshotId: number;
  command: GeometryCommand;
}) {
  const { snapshotId, command } = args;

  if (!snapshotId) {
    return { ok: false, error: { kind: "invalid", detail: "snapshotId required" } };
  }

  switch (command.command) {
    case "TRANSLATE":
      return executeTool({
        snapshotId,
        station: "geometry",
        tool: "translate",
        payload: {
          target_id: command.target_id,
          delta: command.delta,
        },
        mode: "proposals",
        enablePreview: false,
      });

    case "ROTATE":
      return executeTool({
        snapshotId,
        station: "geometry",
        tool: "rotate",
        payload: {
          target_id: command.target_id,
          axis: command.axis,
          degrees: command.degrees,
        },
        mode: "proposals",
        enablePreview: false,
      });

    case "SCALE":
      return executeTool({
        snapshotId,
        station: "geometry",
        tool: "scale",
        payload: {
          target_id: command.target_id,
          axis: command.axis,
          factor: command.factor,
        },
        mode: "proposals",
        enablePreview: false,
      });

    default:
      return {
        ok: false,
        error: { kind: "invalid", detail: `Unsupported command: ${(command as any).command}` },
      };
  }
}
