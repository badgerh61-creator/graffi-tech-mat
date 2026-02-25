// frontend/src/editor/gizmo/TransformGizmo.jsx

import { useMemo, useState } from "react";
import {
  buildTranslatePayload,
  buildRotatePayload,
  buildScalePayload,
} from "./payloadBuilders";

import PivotControls from "../transform/PivotControls";
import SnapControls from "../transform/SnapControls";

export default function TransformGizmo({
  enabled,
  reasonDisabled,
  activeTargetId,
  onCommit,
}) {
  // =========================
  // Mode
  // =========================
  const [mode, setMode] = useState("translate"); // translate | rotate | scale

  // =========================
  // Snap State (Tier 7.24 shared)
  // =========================
  const [snapEnabled, setSnapEnabled] = useState(true);

  const [snapStepTranslate, setSnapStepTranslate] = useState(0.25);
  const [snapStepDegrees, setSnapStepDegrees] = useState(5);
  const [snapStepFactor, setSnapStepFactor] = useState(0.05);

  // =========================
  // Pivot State (Tier 7.22)
  // =========================
  const [pivotMode, setPivotMode] = useState("bbox_center");
  const [customPivot, setCustomPivot] = useState({ x: 0, y: 0, z: 0 });

  const canShow = !!activeTargetId;

  const statusText = useMemo(() => {
    if (!canShow) return "No target selected";
    if (enabled) return `Gizmo enabled (${mode})`;
    return `Gizmo disabled: ${reasonDisabled || "blocked"}`;
  }, [canShow, enabled, reasonDisabled, mode]);

  if (!canShow) return null;

  // =========================
  // Commit Helpers
  // =========================

  const commitTranslate = (axis, sign) => {
    const invocation = buildTranslatePayload({
      targetId: activeTargetId,
      axis,
      rawDelta:
        axis === "x"
          ? { x: 0.1 * sign, y: 0, z: 0 }
          : axis === "y"
          ? { x: 0, y: 0.1 * sign, z: 0 }
          : { x: 0, y: 0, z: 0.1 * sign },
      snap: { enabled: snapEnabled, step: snapStepTranslate },
    });

    onCommit?.({
      ...invocation,
      __ui: {
        pivotMode,
        customPivot,
        snapEnabled,
        snapStep: snapStepTranslate,
      },
    });
  };

  const commitRotate = (axis, sign) => {
    const invocation = buildRotatePayload({
      targetId: activeTargetId,
      axis,
      rawDegrees: 10 * sign,
      snap: { enabled: snapEnabled, step_degrees: snapStepDegrees },
    });

    onCommit?.({
      ...invocation,
      __ui: {
        pivotMode,
        customPivot,
        snapEnabled,
        snapStepDegrees,
      },
    });
  };

  const commitScale = (axis, sign) => {
    const factor = sign > 0 ? 1.1 : 0.9;

    const invocation = buildScalePayload({
      targetId: activeTargetId,
      axis,
      rawFactor: factor,
      snap: { enabled: snapEnabled, step_factor: snapStepFactor },
    });

    onCommit?.({
      ...invocation,
      __ui: {
        pivotMode,
        customPivot,
        snapEnabled,
        snapStepFactor,
      },
    });
  };

  // =========================
  // Snap UI Config (dynamic per mode)
  // =========================

  const snapStep =
    mode === "translate"
      ? snapStepTranslate
      : mode === "rotate"
      ? snapStepDegrees
      : snapStepFactor;

  const setSnapStep =
    mode === "translate"
      ? setSnapStepTranslate
      : mode === "rotate"
      ? setSnapStepDegrees
      : setSnapStepFactor;

  const snapLabel =
    mode === "translate"
      ? "Grid step"
      : mode === "rotate"
      ? "Degree step"
      : "Scale step";

  const snapInputStep =
    mode === "translate"
      ? 0.05
      : mode === "rotate"
      ? 1
      : 0.01;

  // =========================
  // Render
  // =========================

  return (
    <div className="rounded-xl border p-3 text-sm space-y-3">
      <div className="font-semibold">Transform Gizmo</div>
      <div className="opacity-80">{statusText}</div>

      {/* Mode Selector */}
      <div className="flex items-center gap-2">
        <span className="text-xs opacity-70">Mode</span>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          disabled={!enabled}
          className="border rounded px-2 py-1 text-sm"
        >
          <option value="translate">Translate</option>
          <option value="rotate">Rotate</option>
          <option value="scale">Scale</option>
        </select>
      </div>

      {/* Snap Controls */}
      <SnapControls
        enabled={snapEnabled}
        setEnabled={setSnapEnabled}
        step={snapStep}
        setStep={setSnapStep}
        label="Snapping"
        stepLabel={snapLabel}
        stepInputStep={snapInputStep}
        disabled={!enabled}
      />

      {/* Pivot Controls */}
      <PivotControls
        pivotMode={pivotMode}
        setPivotMode={setPivotMode}
        customPivot={customPivot}
        setCustomPivot={setCustomPivot}
        disabled={!enabled}
      />

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-2">
        {mode === "translate" && (
          <>
            <button className="border rounded px-3 py-1" onClick={() => commitTranslate("x", -1)} disabled={!enabled}>
              Nudge -X
            </button>
            <button className="border rounded px-3 py-1" onClick={() => commitTranslate("x", +1)} disabled={!enabled}>
              Nudge +X
            </button>
          </>
        )}

        {mode === "rotate" && (
          <>
            <button className="border rounded px-3 py-1" onClick={() => commitRotate("y", -1)} disabled={!enabled}>
              Rotate -Y
            </button>
            <button className="border rounded px-3 py-1" onClick={() => commitRotate("y", +1)} disabled={!enabled}>
              Rotate +Y
            </button>
          </>
        )}

        {mode === "scale" && (
          <>
            <button className="border rounded px-3 py-1" onClick={() => commitScale("uniform", -1)} disabled={!enabled}>
              Scale -
            </button>
            <button className="border rounded px-3 py-1" onClick={() => commitScale("uniform", +1)} disabled={!enabled}>
              Scale +
            </button>
          </>
        )}
      </div>

      <div className="text-xs opacity-70">
        UI-only: emits governed tool payloads. Kernel execution via controller.
      </div>
    </div>
  );
}
