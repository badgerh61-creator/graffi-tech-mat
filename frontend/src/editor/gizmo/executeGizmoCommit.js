import { executeTool } from "../../services/studio/toolExecutionAdapter";

/**
 * One place to send a gizmo commit payload into governed pipeline.
 * Assumes payload like:
 * { tool, station, payload: { target_id, ... }, snapshotId? }
 */
export async function executeGizmoCommit(payload) {
  const snapshotId = payload?.snapshotId ?? payload?.snapshot_id;
  const station = payload?.station || "geometry";
  const tool = payload?.tool;
  const toolPayload = payload?.payload || {};

  if (!snapshotId) {
    return {
      ok: false,
      error: { kind: "invalid", detail: "snapshotId required" },
    };
  }

  if (!tool) {
    return {
      ok: false,
      error: { kind: "invalid", detail: "tool required" },
    };
  }

  return await executeTool({
    snapshotId,
    station,
    tool,
    payload: toolPayload,
    mode: "proposals",
    enablePreview: false,
  });
}
