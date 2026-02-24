import type { SelectionState } from "../selection/selectionTypes";
import { buildSelectedTargetIds } from "../selection/buildSelectedTargetIds";
import { computeSelectionBboxStub } from "../selection/computeSelectionBboxStub";

export type GizmoContext = {
  target_id: string;
  selected_target_ids?: string[];
  pivot_mode?: "bbox_center" | "world_origin" | "custom";
  pivot?: { x: number; y: number; z: number };
  selection_bbox?: {
    min: { x: number; y: number; z: number };
    max: { x: number; y: number; z: number };
  };
};

export function buildGizmoContext(opts: {
  selection: SelectionState;
  pivotMode: "bbox_center" | "world_origin" | "custom";
  customPivot: { x: number; y: number; z: number };
}): GizmoContext | null {
  const primary = opts.selection.primary?.id;
  if (!primary) return null;

  const ids = buildSelectedTargetIds(opts.selection);
  const isMulti = ids.length > 1;

  const bbox = isMulti ? computeSelectionBboxStub(ids) : null;

  return {
    target_id: primary,
    selected_target_ids: isMulti ? ids : undefined,
    pivot_mode: isMulti ? opts.pivotMode : undefined,
    pivot: isMulti && opts.pivotMode === "custom" ? opts.customPivot : undefined,
    selection_bbox: isMulti && bbox ? bbox : undefined,
  };
}
