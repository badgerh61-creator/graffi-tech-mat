import React from "react";
import { useMemo, useState } from "react";
import { getAccessToken } from "../../utils/auth";
import { getTelemetrySummary, compareTelemetry, exportTelemetryCsv } from "../../services/telemetryReportsApi";

function fmt(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return "—";
  return x.toFixed(3);
}

export default function TelemetryComparePanel() {
  const token = useMemo(() => getAccessToken?.(), []);

  const [aId, setAId] = useState("");
  const [bId, setBId] = useState("");

  const [aSum, setASum] = useState(null);
  const [bSum, setBSum] = useState(null);
  const [delta, setDelta] = useState(null);

  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);

  async function onCompare() {
    setBusy(true); setErr(null);
    try {
      const a = await getTelemetrySummary({ artifactId: Number(aId), token });
      const b = await getTelemetrySummary({ artifactId: Number(bId), token });
      const d = await compareTelemetry({ aArtifactId: Number(aId), bArtifactId: Number(bId), token });

      setASum(a);
      setBSum(b);
      setDelta(d);
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  async function exportA() {
    setErr(null);
    try {
      const csv = await exportTelemetryCsv({ artifactId: Number(aId), token });
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `telemetry-${aId}.csv`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setErr(String(e?.message || e));
    }
  }

  const metricKeys = useMemo(() => {
    const s = aSum?.summary || {};
    return Object.keys(s).filter((k) => k !== "duration_s" && k !== "timestep_s").sort();
  }, [aSum]);

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="text-sm font-semibold">Telemetry Compare (6S.4)</div>

      <div className="grid grid-cols-2 gap-2">
        <label className="text-xs">
          A artifact_id
          <input
            className="border rounded w-full px-2 py-1"
            value={aId}
            onChange={(e) => setAId(e.target.value)}
            aria-label="A artifact_id"
          />
        </label>
        <label className="text-xs">
          B artifact_id
          <input
            className="border rounded w-full px-2 py-1"
            value={bId}
            onChange={(e) => setBId(e.target.value)}
            aria-label="B artifact_id"
          />
        </label>
      </div>

      <div className="flex gap-2">
        <button className="border rounded px-3 py-1 text-sm" onClick={onCompare} disabled={busy || !aId || !bId}>
          {busy ? "Loading..." : "Compare"}
        </button>
        <button className="border rounded px-3 py-1 text-sm" onClick={exportA} disabled={!aId}>
          Export A CSV
        </button>
      </div>

      {err ? <div className="text-xs border rounded p-2">Error: {err}</div> : null}

      {aSum?.summary && bSum?.summary ? (
        <div className="grid grid-cols-3 gap-2 text-xs" role="table" aria-label="compare-table">
          <div className="border rounded p-2">
            <div className="font-semibold">Metric</div>
            {metricKeys.map((k) => <div key={k} className="opacity-80">{k}</div>)}
          </div>
          <div className="border rounded p-2">
            <div className="font-semibold">A</div>
            {metricKeys.map((k) => <div key={k}>{fmt(aSum.summary[k])}</div>)}
          </div>
          <div className="border rounded p-2">
            <div className="font-semibold">Δ (B - A)</div>
            {delta?.delta
              ? Object.keys(delta.delta).sort().map((k) => <div key={k}>{fmt(delta.delta[k])}</div>)
              : <div className="opacity-70">—</div>}
          </div>
        </div>
      ) : (
        <div className="text-xs opacity-70">Enter two artifact ids and compare.</div>
      )}
    </div>
  );
}
