import { clearSelection } from "../selection/selectionStore";
import { clearGizmoPreview } from "../gizmo/gizmoPreviewStore";

/**
 * Tier 7.31
 * One canonical navigation function.
 *
 * setActiveSnapshotId: function(number)
 */
export function navigateToSnapshot({ snapshotId, setActiveSnapshotId }) {
  const id = Number(snapshotId);
  if (!Number.isFinite(id)) return;

  // clear volatile UI state (must not drift across snapshots)
  clearGizmoPreview?.();
  clearSelection?.();

  // switch snapshot
  setActiveSnapshotId(id);
}
