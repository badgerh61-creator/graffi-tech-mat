export type SnapValidation =
  | { ok: true }
  | { ok: false; reason: "invalid_snap_step" };

export function validateSnap(enabled: boolean, step: number): SnapValidation {
  if (!enabled) return { ok: true };
  if (typeof step !== "number" || !Number.isFinite(step) || step <= 0) {
    return { ok: false, reason: "invalid_snap_step" };
  }
  return { ok: true };
}
