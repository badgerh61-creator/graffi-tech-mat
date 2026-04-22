import { getAccessToken } from "../../utils/auth";

const API = "/api";

export async function fetchScene(snapshotId) {
  const token = getAccessToken?.();

  const res = await fetch(`${API}/snapshots/${snapshotId}/scene`, {
    headers: token
      ? { Authorization: `Bearer ${token}` }
      : {},
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to fetch scene: ${res.status} ${text}`);
  }

  return res.json();
}
