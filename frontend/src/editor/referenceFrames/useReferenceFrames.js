import { API_BASE } from "../../config/apiBase";

import { useEffect, useState } from "react";
import { getAccessToken } from "../../utils/auth";

export function useReferenceFrames(snapshotId) {
  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!snapshotId) return;

    const token = getAccessToken();

    fetch(`${API_BASE}/snapshots/${snapshotId}/reference-frames`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
        return res.json();
      })
      .then(setData)
      .catch(setErr);
  }, [snapshotId]);

  return { data, err };
}
