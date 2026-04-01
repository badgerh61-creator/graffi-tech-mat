import { getAccessToken } from "../../utils/auth";

const API = "http://127.0.0.1:8000";

export async function fetchScene(snapshotId) {
  const token = getAccessToken?.();

  const res = await fetch(`${API}/snapshots/${snapshotId}/scene`, {
    headers: token
      ? { Authorization: `Bearer ${token}` }
      : {},
  });

  if (!res.ok) {
    throw new Error("Failed to fetch scene");
  }

  return res.json();
}
