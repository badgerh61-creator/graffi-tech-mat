import { toolExecutionAdapter } from "../../services/studio/toolExecutionAdapter";

/**
 * One place to send a gizmo commit payload into governed pipeline.
 * Assumes payload like:
 * { tool, station, payload: { target_id, ... } }
 */
export async function executeGizmoCommit(payload) {
  // you already have this pattern in Tier 7.8
  // evaluate -> apply
  const evaluated = await toolExecutionAdapter.evaluate(payload);
  if (!evaluated?.ok) return evaluated;
  return await toolExecutionAdapter.apply(evaluated.proposal_id);
}
