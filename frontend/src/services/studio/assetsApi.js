// frontend/src/services/studio/assetsApi.js

import { getAccessToken } from "../../utils/auth";

const API_BASE = "http://127.0.0.1:8000";

function authHeaders(extra = {}) {
  const token = getAccessToken?.();
  return {
    ...extra,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

// Optional helper if you want to inspect auth status quickly in DevTools
function publishDbg(key, value) {
  try {
    window[key] = value;
  } catch {}
}

/**
 * GET /assets/
 * Returns: { items, total } (per your backend)
 */
export async function listAssets() {
  const url = `${API_BASE}/assets/`;

  publishDbg("__dbg_listAssets_request", { url });

  const res = await fetch(url, {
    headers: authHeaders(),
  });

  const text = await res.text();

  publishDbg("__dbg_listAssets_response", {
    ok: res.ok,
    status: res.status,
    text,
  });

  if (!res.ok) throw new Error(text || `Failed to list assets (${res.status})`);

  try {
    const data = JSON.parse(text);
    return data; // { items, total }
  } catch {
    // Keep caller stable even if backend returned non-json
    return { items: [], total: 0 };
  }
}

/**
 * POST /projects/:projectId/snapshots/:snapshotId/tools/attach-asset
 * Payload: { object_id, asset_id, kind }
 *
 * NOTE: This will only succeed on DRAFT snapshots (as your UI indicates).
 */
export async function attachAsset(projectId, snapshotId, payload) {
  const url = `${API_BASE}/projects/${projectId}/snapshots/${snapshotId}/tools/attach-asset`;

  // Debug publish
  publishDbg("__dbg_attachAsset_request", {
    url,
    projectId,
    snapshotId,
    payload,
  });

  const res = await fetch(url, {
    method: "POST",
    headers: authHeaders({ "Content-Type": "application/json" }),
    body: JSON.stringify(payload),
  });

  const text = await res.text();

  // Debug publish
  publishDbg("__dbg_attachAsset_response", {
    ok: res.ok,
    status: res.status,
    text,
  });

  if (!res.ok) throw new Error(text || `Failed to attach asset (${res.status})`);

  try {
    return JSON.parse(text);
  } catch {
    return { ok: true };
  }
}
