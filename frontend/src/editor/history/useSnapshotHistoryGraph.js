import { useEffect, useState } from "react";

import { API_BASE } from "../../config/apiBase";

export function useSnapshotHistoryGraph(snapshotId) {
  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!snapshotId) return;

    let cancelled = false;
    setLoading(true);
    setErr(null);

    fetch(`${API_BASE}/snapshots/${snapshotId}/history`)
      .then(async (res) => {
        const body = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(body?.detail || `history failed: ${res.status}`);
        return body;
      })
      .then((body) => !cancelled && setData(body))
      .catch((e) => !cancelled && setErr(e))
      .finally(() => !cancelled && setLoading(false));

    return () => { cancelled = true; };
  }, [snapshotId]);

  return { data, err, loading };
}
