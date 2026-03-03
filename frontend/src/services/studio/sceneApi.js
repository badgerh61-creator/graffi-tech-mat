// frontend/src/services/studio/sceneApi.js
import { getAccessToken } from "../../utils/auth";
import { executeTool } from "./toolExecutionAdapter";

const API_BASE = "http://127.0.0.1:8000";

/**
 * fetchScene(projectId, snapshotId, { signal })
 * - supports AbortController to prevent stale fetch overwrites
 */
export async function fetchScene(projectId, snapshotId, opts = {}) {
  const token = getAccessToken?.();
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const res = await fetch(
    `${API_BASE}/projects/${projectId}/snapshots/${snapshotId}/scene`,
    {
      signal: opts.signal,
      headers,
    }
  );

  if (!res.ok) throw new Error(`Failed to load scene (${res.status})`);
  return await res.json();
}

/**
 * Tier 7.46 — Scene Objects (governed)
 * Adds a model_ref object into snapshot.body_state.objects
 *
 * Returns executeTool normalized result:
 * { ok: true, data } | { ok: false, error }
 */
export async function addModelRefToScene({
  snapshotId,
  assetId,
  name,
  transform,
  enablePreview = false,
}) {
  return await executeTool({
    snapshotId,
    station: "geometry",
    tool: "SCENE_ADD_MODEL_REF",
    payload: {
      asset_id: assetId,
      name: name || null,
      transform: transform || null,
    },
    mode: "proposals",
    enablePreview,
  });
}

/**
 * Tier 7.46 — Scene Objects (governed)
 * Removes an object from snapshot.body_state.objects
 */
export async function removeSceneObject({
  snapshotId,
  objectId,
  enablePreview = false,
}) {
  return await executeTool({
    snapshotId,
    station: "geometry",
    tool: "SCENE_REMOVE_OBJECT",
    payload: {
      object_id: objectId,
    },
    mode: "proposals",
    enablePreview,
  });
}
