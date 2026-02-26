import { useMemo, useState } from "react";
import ConstraintViolationsPanel from "../constraints/ConstraintViolationsPanel";

export default function ComponentsPanel({ snapshot, activeTargetId, onCommitApplyComponent }) {
  const comps = useMemo(() => snapshot?.body_state?.components || [], [snapshot]);

  const [selectedComponentId, setSelectedComponentId] = useState(
    comps?.[0]?.id || ""
  );

  const selected = comps.find((c) => String(c.id) === String(selectedComponentId));

  const [deltaY, setDeltaY] = useState(0.0);
  const [degrees, setDegrees] = useState(0.0);
  const [factor, setFactor] = useState(1.0);

  // ✅ Tier 7.32/7.33 UI: show constraint violations returned by /evaluate
  const [violations, setViolations] = useState([]);
  const [evaluateAllowed, setEvaluateAllowed] = useState(true);
  const [evaluateReason, setEvaluateReason] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);

  if (!snapshot) return null;

  const snapshotId = snapshot?.id;

  async function evaluateProposal(proposal) {
    if (!snapshotId) {
      setEvaluateAllowed(false);
      setEvaluateReason("missing_snapshot_id");
      setViolations([]);
      return { allowed: false, violations: [] };
    }

    setIsEvaluating(true);
    try {
      const res = await fetch("/assistant/proposals/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          snapshot_id: snapshotId,
          proposal,
        }),
      });

      const data = await res.json();

      const v = data?.violations || [];
      setViolations(v);
      setEvaluateAllowed(Boolean(data?.allowed));
      setEvaluateReason(data?.reason || null);

      return data;
    } catch (e) {
      setEvaluateAllowed(false);
      setEvaluateReason("evaluate_failed");
      setViolations([]);
      return { allowed: false, violations: [] };
    } finally {
      setIsEvaluating(false);
    }
  }

  async function handleApply(proposal) {
    // Evaluate first to get constraint violations for UI
    const data = await evaluateProposal(proposal);
    if (!data?.allowed) return;

    // Only commit if evaluate allowed
    onCommitApplyComponent?.(proposal);
  }

  const canApply = !isEvaluating && evaluateAllowed && !(violations?.length);

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Parametric Components</div>

      <div className="text-xs opacity-70">
        Target: {activeTargetId || "none"}
      </div>

      <select
        className="border rounded px-2 py-1 text-sm w-full"
        value={selectedComponentId}
        onChange={(e) => {
          setSelectedComponentId(e.target.value);
          // reset UI feedback when switching component
          setViolations([]);
          setEvaluateAllowed(true);
          setEvaluateReason(null);
        }}
      >
        {comps.map((c) => (
          <option key={c.id} value={c.id}>
            {c.kind} — {c.name || c.id}
          </option>
        ))}
      </select>

      {!selected ? (
        <div className="text-xs opacity-70">No component selected.</div>
      ) : (
        <div className="space-y-2">
          <div className="text-xs opacity-70">kind: {selected.kind}</div>

          {selected.kind === "ride_height" ? (
            <>
              <label className="text-sm flex items-center justify-between gap-2">
                <span>delta_y</span>
                <input
                  className="border rounded px-2 py-1 w-28"
                  type="number"
                  step="0.05"
                  value={deltaY}
                  onChange={(e) => setDeltaY(parseFloat(e.target.value || "0"))}
                />
              </label>

              <button
                className="border rounded px-3 py-2 text-sm disabled:opacity-50"
                disabled={!canApply}
                onClick={() =>
                  handleApply({
                    tool: "APPLY_COMPONENT",
                    station: "geometry",
                    payload: {
                      component_id: selected.id,
                      next_params: { delta_y: deltaY },
                      target_id: activeTargetId || selected.target_id || null,
                    },
                  })
                }
              >
                {isEvaluating ? "Evaluating..." : "Apply Component"}
              </button>
            </>
          ) : selected.kind === "spoiler_angle" ? (
            <>
              <label className="text-sm flex items-center justify-between gap-2">
                <span>degrees</span>
                <input
                  className="border rounded px-2 py-1 w-28"
                  type="number"
                  step="1"
                  value={degrees}
                  onChange={(e) => setDegrees(parseFloat(e.target.value || "0"))}
                />
              </label>

              <button
                className="border rounded px-3 py-2 text-sm disabled:opacity-50"
                disabled={!canApply}
                onClick={() =>
                  handleApply({
                    tool: "APPLY_COMPONENT",
                    station: "geometry",
                    payload: {
                      component_id: selected.id,
                      next_params: { degrees },
                      target_id: activeTargetId || selected.target_id || null,
                    },
                  })
                }
              >
                {isEvaluating ? "Evaluating..." : "Apply Component"}
              </button>
            </>
          ) : selected.kind === "wheel_scale" ? (
            <>
              <label className="text-sm flex items-center justify-between gap-2">
                <span>factor</span>
                <input
                  className="border rounded px-2 py-1 w-28"
                  type="number"
                  step="0.05"
                  value={factor}
                  onChange={(e) => setFactor(parseFloat(e.target.value || "1"))}
                />
              </label>

              <button
                className="border rounded px-3 py-2 text-sm disabled:opacity-50"
                disabled={!canApply}
                onClick={() =>
                  handleApply({
                    tool: "APPLY_COMPONENT",
                    station: "geometry",
                    payload: {
                      component_id: selected.id,
                      next_params: { factor },
                      target_id: activeTargetId || selected.target_id || null,
                    },
                  })
                }
              >
                {isEvaluating ? "Evaluating..." : "Apply Component"}
              </button>
            </>
          ) : (
            <div className="text-xs opacity-70">
              Unknown kind (no UI yet). Safe.
            </div>
          )}

          {/* ✅ If kernel rejects for any reason, show a tiny reason line */}
          {!evaluateAllowed && evaluateReason ? (
            <div className="text-xs text-red-700">
              Blocked: {String(evaluateReason)}
            </div>
          ) : null}

          {/* ✅ Constraint violations UI */}
          <ConstraintViolationsPanel violations={violations} />
        </div>
      )}
    </div>
  );
}
