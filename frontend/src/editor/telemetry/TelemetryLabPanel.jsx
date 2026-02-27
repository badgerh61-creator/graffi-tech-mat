// frontend/src/editor/telemetry/TelemetryLabPanel.jsx
import { useEffect, useMemo, useState } from "react";
import { getAccessToken } from "../../utils/auth";
import {
  createScenario,
  listScenarios,
  runScenario,
  listRuns,
  compareMatrix,
} from "../../services/simulationLabApi";

// Tier 6S.9 (read-only trust badge). Safe: if you haven't added it yet, remove this import.
import ReproBadge from "./ReproBadge";

export default function TelemetryLabPanel({ projectId, activeSnapshot }) {
  const token = useMemo(() => getAccessToken?.(), []);
  const [scenarios, setScenarios] = useState([]);
  const [runs, setRuns] = useState([]);

  const [newName, setNewName] = useState("Baseline");
  const [newThrottle, setNewThrottle] = useState(0.6);

  const [selectedScenarioId, setSelectedScenarioId] = useState("");
  const [selectedArtifacts, setSelectedArtifacts] = useState([]);
  const [matrix, setMatrix] = useState(null);

  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);

  async function refresh() {
    if (!projectId) return;
    setErr(null);
    const s = await listScenarios({ projectId, token });
    const r = await listRuns({ projectId, token });
    setScenarios(s.scenarios || []);
    setRuns(r.runs || []);
  }

  useEffect(() => {
    refresh().catch((e) => setErr(String(e?.message || e)));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId]);

  async function onCreateScenario() {
    setBusy(true);
    setErr(null);
    try {
      await createScenario({
        projectId,
        name: newName,
        scenario: { throttle: Number(newThrottle), duration_s: 10.0, timestep_s: 0.1 },
        token,
      });
      await refresh();
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  async function onRunScenario() {
    if (!activeSnapshot?.id || !selectedScenarioId) return;
    setBusy(true);
    setErr(null);
    try {
      await runScenario({
        snapshotId: activeSnapshot.id,
        engineVersion: "pseudo-v1",
        scenarioId: Number(selectedScenarioId),
        token,
      });
      await refresh();
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  function toggleArtifact(id) {
    const s = new Set(selectedArtifacts);
    if (s.has(id)) s.delete(id);
    else s.add(id);
    setSelectedArtifacts(Array.from(s).sort((a, b) => a - b));
  }

  async function onBuildMatrix() {
    setBusy(true);
    setErr(null);
    try {
      const out = await compareMatrix({ artifactIds: selectedArtifacts, token });
      setMatrix(out);
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="text-sm font-semibold">Telemetry Lab (6S.5)</div>
      {err ? <div className="text-xs border rounded p-2">Error: {err}</div> : null}

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold">Create Scenario</div>
        <div className="grid grid-cols-2 gap-2">
          <input
            className="border rounded px-2 py-1 text-sm"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
          />
          <input
            className="border rounded px-2 py-1 text-sm"
            type="number"
            value={newThrottle}
            onChange={(e) => setNewThrottle(e.target.value)}
          />
        </div>
        <button
          className="border rounded px-3 py-1 text-sm"
          disabled={busy || !projectId}
          onClick={onCreateScenario}
        >
          Save Scenario
        </button>
      </div>

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold">Run Scenario</div>
        <select
          className="border rounded px-2 py-1 text-sm w-full"
          value={selectedScenarioId}
          onChange={(e) => setSelectedScenarioId(e.target.value)}
        >
          <option value="">Select scenario…</option>
          {scenarios.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} (id:{s.id})
            </option>
          ))}
        </select>

        <button
          className="border rounded px-3 py-1 text-sm"
          disabled={busy || !activeSnapshot?.id || !selectedScenarioId}
          onClick={onRunScenario}
        >
          Run (creates artifact)
        </button>
      </div>

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold">Runs</div>
        <div className="text-xs opacity-70">Select ≥2 artifacts to build compare matrix.</div>

        <div className="space-y-2">
          {runs.map((r) => (
            <div key={r.run_id} className="border rounded p-2">
              <label className="text-xs flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={selectedArtifacts.includes(r.artifact_id)}
                  onChange={() => toggleArtifact(r.artifact_id)}
                />
                <span>
                  run:{r.run_id} artifact:{r.artifact_id} snap:{r.snapshot_id} scenario:{r.scenario_id ?? "—"} engine:
                  {r.engine_version}
                </span>
              </label>

              {/* Tier 6S.9: reproducibility badge (read-only). Safe even if older runs have empty hashes */}
              <div className="mt-2">
                <ReproBadge runId={r.run_id} />
              </div>
            </div>
          ))}
        </div>

        <button
          className="border rounded px-3 py-1 text-sm"
          disabled={busy || selectedArtifacts.length < 2}
          onClick={onBuildMatrix}
        >
          Build Compare Matrix
        </button>
      </div>

      {matrix ? (
        <div className="border rounded p-2 space-y-2">
          <div className="text-xs font-semibold">Matrix (Δ = B - A)</div>
          <div className="text-xs opacity-70">Pairs are "A-B" by artifact_id.</div>
          <div className="text-xs font-mono whitespace-pre overflow-auto">
            {JSON.stringify(matrix.matrix, null, 2)}
          </div>
        </div>
      ) : null}
    </div>
  );
}
