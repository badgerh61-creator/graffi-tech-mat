import { getAccessToken } from "../../utils/auth";

const API = "http://localhost:8000";

export async function bootstrapEditSession(projectId) {
  const token = getAccessToken?.();

  const headers = token
    ? { Authorization: `Bearer ${token}` }
    : {};

  // 1. fetch snapshots
  const res = await fetch(`${API}/projects/${projectId}/snapshots`, {
    headers,
  });

  if (!res.ok) throw new Error("Failed to fetch snapshots");

  const snapshots = await res.json();

  if (!snapshots.length) {
    throw new Error("No snapshots available");
  }

  // 2. pick base snapshot (latest completed)
  const base =
    snapshots.find((s) => s.status === "completed") || snapshots[0];

  // 3. create draft (or reuse)
  const draftRes = await fetch(
    `${API}/projects/${projectId}/snapshots/${base.id}/draft`,
    {
      method: "POST",
      headers,
    }
  );

  let draftId;

  if (draftRes.ok) {
    const data = await draftRes.json();
    draftId = data.id;
  } else {
    // fallback → find existing draft
    const existing = snapshots.find((s) => s.status === "draft");

    if (!existing) {
      throw new Error("Draft creation failed and none found");
    }

    draftId = existing.id;
  }

  // 4. acquire lock
  const lockRes = await fetch(
    `${API}/projects/${projectId}/snapshots/${draftId}/lock`,
    {
      method: "POST",
      headers,
    }
  );

  if (!lockRes.ok) {
    console.warn("Lock not acquired (maybe already locked)");
  }

  return draftId;
}
