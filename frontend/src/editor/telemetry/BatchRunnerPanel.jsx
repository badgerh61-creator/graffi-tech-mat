import { useMemo, useState } from "react";
import { getAccessToken } from "../../utils/auth";
import { createBatch, getBatchStatus } from "../../services/simulationBatchApi";

export default function BatchRunnerPanel({ activeSnapshot }) {
  const token = useMemo(() => getAccessToken?.(), []);
  const [templateKeys, setTemplateKeys] = useState("accel_0_60_v1,thermal_load_v1");
  const [batch, setBatch] = useState(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  async function runBatch() {
    if (!activeSnapshot?.id) return;
    setBusy(true); setErr(null);
    try {
      const keys = templateKeys
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);

      const out = await createBatch({
        snapshotId: activeSnapshot.id,
        engineVersion: "pseudo-v1",
        templateKeys: keys,
        token,
      });
      setBatch(out);
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  async function refreshStatus() {
    if (!batch?.batch_id) return;
    setBusy(true); setErr(null);
    try {
      const st = await getBatchStatus({ batchId: batch.batch_id, token });
      setBatch((prev) => ({ ...prev, ...st }));
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Batch Runner (6S.7)</div>

      {err ? <div className="text-xs border rounded p-2">Error: {err}</div> : null}

      <label className="text-xs">
        Template keys (comma separated)
        <input
          className="border rounded w-full px-2 py-1"
          value={templateKeys}
          onChange={(e) => setTemplateKeys(e.target.value)}
        />
      </label>

      <div className="flex gap-2">
        <button className="border rounded px-3 py-1 text-sm" disabled={busy || !activeSnapshot?.id} onClick={runBatch}>
          {busy ? "Running..." : "Run Batch"}
        </button>
        <button className="border rounded px-3 py-1 text-sm" disabled={busy || !batch?.batch_id} onClick={refreshStatus}>
          Refresh Status
        </button>
      </div>

      {batch ? (
        <div className="text-xs border rounded p-2 space-y-1">
          <div>batch: {batch.batch_id}</div>
          <div>status: {batch.status}</div>
          <div>artifacts: {(batch.artifact_ids || []).join(", ") || "—"}</div>
          {batch.error ? <div className="opacity-80">error: {batch.error}</div> : null}
        </div>
      ) : (
        <div className="text-xs opacity-70">No batch yet.</div>
      )}
    </div>
  );
}
