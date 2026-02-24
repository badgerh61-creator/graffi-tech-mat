import { resolvePrimaryTarget } from "../selection/resolveTarget";

/**
 * Tool Preflight Guard (Tier 7.14)
 *
 * Returns:
 *  - { ok: true, target_id }
 *  - { ok: false, reason: "no_selection"|"no_snapshot"|"ui_disabled" }
 */
export function toolPreflightGuard({ selection, uiDisabled, activeSnapshotId }) {
  if (uiDisabled) return { ok: false, reason: "ui_disabled" };
  if (!activeSnapshotId) return { ok: false, reason: "no_snapshot" };

  const rt = resolvePrimaryTarget(selection);
  if (!rt.ok) return { ok: false, reason: "no_selection" };

  return { ok: true, target_id: rt.target_id };
}
