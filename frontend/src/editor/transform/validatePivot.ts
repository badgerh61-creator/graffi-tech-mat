export type PivotMode = "bbox_center" | "world_origin" | "custom";
export type Pivot = { x: number; y: number; z: number };

export type PivotValidation =
  | { ok: true }
  | { ok: false; reason: "invalid_pivot" };

function isFiniteNumber(v: unknown): v is number {
  return typeof v === "number" && Number.isFinite(v);
}

export function validatePivot(pivotMode: PivotMode, pivot: Pivot): PivotValidation {
  if (pivotMode !== "custom") return { ok: true };

  if (!isFiniteNumber(pivot?.x) || !isFiniteNumber(pivot?.y) || !isFiniteNumber(pivot?.z)) {
    return { ok: false, reason: "invalid_pivot" };
  }

  return { ok: true };
}
