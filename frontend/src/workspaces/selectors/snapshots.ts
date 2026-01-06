/**
 * Phase J.5 — Snapshot selectors
 * Read-only helpers
 */

export function getLatestCompletedSnapshot(snapshots: {
  completed: any[];
  failed: any[];
  pending: any[];
}) {
  return snapshots.completed?.[0] ?? null;
}

export function getFailedSnapshots(snapshots: {
  completed: any[];
  failed: any[];
  pending: any[];
}) {
  return snapshots.failed ?? [];
}

