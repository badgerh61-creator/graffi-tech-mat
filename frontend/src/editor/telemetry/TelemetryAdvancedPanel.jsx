// frontend/src/editor/telemetry/TelemetryAdvancedPanel.jsx
import React from "react";
import { useMemo, useState } from "react";
import { getAccessToken } from "../../utils/auth";
import { getTelemetryArtifact } from "../../services/simulationApi";
import {
  useTelemetry,
  addArtifact,
  removeArtifact,
  toggleCurve,
} from "./telemetryStore";
import { normalizeRuns, toPolyline } from "./multiChart";

export default function TelemetryAdvancedPanel() {
  const { artifacts, visibleCurves } = useTelemetry();
  const [artifactIdInput, setArtifactIdInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  const curveNames = useMemo(() => {
    const set = new Set();
    for (const a of artifacts) {
      for (const k of Object.keys(a.curves || {})) {
        if (k !== "time_s") set.add(k);
      }
    }
    return Array.from(set).sort();
  }, [artifacts]);

  async function onLoadArtifact() {
    const id = Number(artifactIdInput);
    if (!Number.isFinite(id) || id <= 0) return;

    setBusy(true);
    setErr(null);
    try {
      const token = getAccessToken?.();
      const art = await getTelemetryArtifact({ artifactId: id, token });
      addArtifact(art);
      setArtifactIdInput("");
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="text-sm font-semibold">Advanced Telemetry (6S.3)</div>

      <div className="flex items-center gap-2">
        <input
          className="border rounded px-2 py-1 text-sm w-40"
          placeholder="artifact id"
          value={artifactIdInput}
          onChange={(e) => setArtifactIdInput(e.target.value)}
        />
        <button
          className="border rounded px-3 py-1 text-sm"
          onClick={onLoadArtifact}
          disabled={busy || !artifactIdInput}
        >
          {busy ? "Loading..." : "Load Artifact"}
        </button>
      </div>

      {err ? <div className="text-xs border rounded p-2">Error: {err}</div> : null}

      {artifacts.length === 0 ? (
        <div className="text-xs opacity-70">
          Load one or more artifacts to compare runs.
        </div>
      ) : (
        <>
          <div className="text-xs">
            <div className="font-semibold mb-1">Runs</div>
            <div className="flex flex-wrap gap-2">
              {artifacts.map((a) => (
                <button
                  key={a.artifact_id}
                  className="border rounded px-2 py-1"
                  onClick={() => removeArtifact(a.artifact_id)}
                  title="Remove run"
                >
                  #{a.artifact_id}
                </button>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            {curveNames.map((c) => (
              <label key={c} className="text-xs flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={!!visibleCurves[c]}
                  onChange={() => toggleCurve(c)}
                />
                {c}
              </label>
            ))}
          </div>

          <div className="space-y-3">
            {curveNames
              .filter((c) => !!visibleCurves[c])
              .map((curve) => {
                const series = normalizeRuns(artifacts, curve);

                return (
                  <div key={curve} className="border rounded p-2">
                    <div className="text-xs font-semibold mb-1">{curve}</div>

                    <svg width="420" height="160" role="img" aria-label={`chart-${curve}`}>
                      {series.map((s) => (
                        <polyline
                          key={s.artifact_id}
                          points={toPolyline(s.points, 420, 160)}
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="1"
                        />
                      ))}
                    </svg>
                  </div>
                );
              })}
          </div>
        </>
      )}
    </div>
  );
}
