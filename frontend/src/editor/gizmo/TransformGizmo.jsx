// frontend/src/editor/gizmo/TransformGizmo.jsx

import { useMemo, useState } from "react";
import {
  buildTranslatePayload,
  buildRotatePayload,
  buildScalePayload,
} from "./payloadBuilders";

import DragPad from "./DragPad";

import PivotControls from "../transform/PivotControls";
import SnapControls from "../transform/SnapControls";

// ✅ Tier 7.27 — preview store + deterministic preview math
import { setGizmoPreview, clearGizmoPreview } from "./gizmoPreviewStore";
import {
  makeTranslatePreview,
  makeRotatePreview,
  makeScalePreview,
} from "./previewMath";

// ✅ Shared gizmo mode (syncs with Three.js TransformControls)
import { useGizmoMode, setGizmoMode } from "./gizmoModeStore";

export default function TransformGizmo({
  enabled,
  reasonDisabled,
  activeTargetId,
  onCommit,
}) {
  // =========================
  // Mode (shared store)
  // =========================
  const { mode } = useGizmoMode(); // translate | rotate | scale

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
  // Deterministic mapping scales (Tier 7.26)
  // =========================
  const TRANSLATE_PER_PX = 0.02; // units per px (tune later)
  const ROTATE_DEG_PER_PX = 0.2; // degrees per px
  const SCALE_PER_PX = 0.005; // factor delta per px

  // =========================
  // Commit Helpers (Drag → one commit)
  // =========================

  function commitTranslateFromDrag(axis, rawDeltaAxis) {
    const rawDelta =
      axis === "x"
        ? { x: rawDeltaAxis, y: 0, z: 0 }
        : axis === "y"
        ? { x: 0, y: rawDeltaAxis, z: 0 }
        : { x: 0, y: 0, z: rawDeltaAxis };

    const invocation = buildTranslatePayload({
      targetId: activeTargetId,
      axis,
      rawDelta,
      snap: { enabled: snapEnabled, step: snapStepTranslate },
    });

    onCommit?.({
      ...invocation,
      __ui: {
        mode: "translate",
        pivotMode,
        customPivot,
        snapEnabled,
        snapStep: snapStepTranslate,
        mapping: { per_px: TRANSLATE_PER_PX },
      },
    });
  }

  function commitRotateFromDrag(axis, rawDegrees) {
    const invocation = buildRotatePayload({
      targetId: activeTargetId,
      axis,
      rawDegrees,
      snap: { enabled: snapEnabled, step_degrees: snapStepDegrees },
    });

    onCommit?.({
      ...invocation,
      __ui: {
        mode: "rotate",
        pivotMode,
        customPivot,
        snapEnabled,
        snapStepDegrees,
        mapping: { deg_per_px: ROTATE_DEG_PER_PX },
      },
    });
  }

  function commitScaleFromDrag(axis, rawFactor) {
    let f = rawFactor;
    if (!Number.isFinite(f)) f = 1;
    f = Math.max(0.01, Math.min(100, f));

    const invocation = buildScalePayload({
      targetId: activeTargetId,
      axis,
      rawFactor: f,
      snap: { enabled: snapEnabled, step_factor: snapStepFactor },
    });

    onCommit?.({
      ...invocation,
      __ui: {
        mode: "scale",
        pivotMode,
        customPivot,
        snapEnabled,
        snapStepFactor,
        mapping: { per_px: SCALE_PER_PX },
      },
    });
  }

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
    mode === "translate" ? 0.05 : mode === "rotate" ? 1 : 0.01;

  // =========================
  // Render
  // =========================

  return (
    <div className="rounded-xl border p-3 text-sm space-y-3">
      <div className="font-semibold">Transform Gizmo</div>
      <div className="opacity-80">{statusText}</div>

      {/* Mode Selector (shared mode store) */}
      <div className="flex items-center gap-2">
        <span className="text-xs opacity-70">Mode</span>
        <select
          value={mode}
          onChange={(e) => {
            setGizmoMode(e.target.value);
            clearGizmoPreview(); // switching modes clears ghost preview
          }}
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
        setEnabled={(v) => {
          setSnapEnabled(v);
          clearGizmoPreview();
        }}
        step={snapStep}
        setStep={(v) => {
          setSnapStep(v);
          clearGizmoPreview();
        }}
        label="Snapping"
        stepLabel={snapLabel}
        stepInputStep={snapInputStep}
        disabled={!enabled}
      />

      {/* Pivot Controls */}
      <PivotControls
        pivotMode={pivotMode}
        setPivotMode={(v) => {
          setPivotMode(v);
          clearGizmoPreview();
        }}
        customPivot={customPivot}
        setCustomPivot={(v) => {
          setCustomPivot(v);
          clearGizmoPreview();
        }}
        disabled={!enabled}
      />

      {/* Drag Pads */}
      {mode === "translate" ? (
        <div className="grid grid-cols-1 gap-2">
          <DragPad
            enabled={enabled}
            label="Translate"
            axisLabel="X"
            mode="translate"
            scale={TRANSLATE_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeTranslatePreview({
                  targetId: activeTargetId,
                  axis: "x",
                  rawDeltaAxis: v,
                  snap: { enabled: snapEnabled, step: snapStepTranslate },
                })
              );
            }}
            onCommit={(v) => {
              clearGizmoPreview();
              commitTranslateFromDrag("x", v);
            }}
          />
          <DragPad
            enabled={enabled}
            label="Translate"
            axisLabel="Y"
            mode="translate"
            scale={TRANSLATE_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeTranslatePreview({
                  targetId: activeTargetId,
                  axis: "y",
                  rawDeltaAxis: v,
                  snap: { enabled: snapEnabled, step: snapStepTranslate },
                })
              );
            }}
            onCommit={(v) => {
              clearGizmoPreview();
              commitTranslateFromDrag("y", v);
            }}
          />
          <DragPad
            enabled={enabled}
            label="Translate"
            axisLabel="Z"
            mode="translate"
            scale={TRANSLATE_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeTranslatePreview({
                  targetId: activeTargetId,
                  axis: "z",
                  rawDeltaAxis: v,
                  snap: { enabled: snapEnabled, step: snapStepTranslate },
                })
              );
            }}
            onCommit={(v) => {
              clearGizmoPreview();
              commitTranslateFromDrag("z", v);
            }}
          />
        </div>
      ) : mode === "rotate" ? (
        <div className="grid grid-cols-1 gap-2">
          <DragPad
            enabled={enabled}
            label="Rotate"
            axisLabel="X"
            mode="rotate"
            scale={ROTATE_DEG_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeRotatePreview({
                  targetId: activeTargetId,
                  axis: "x",
                  rawDegrees: v,
                  snap: { enabled: snapEnabled, step_degrees: snapStepDegrees },
                })
              );
            }}
            onCommit={(deg) => {
              clearGizmoPreview();
              commitRotateFromDrag("x", deg);
            }}
          />
          <DragPad
            enabled={enabled}
            label="Rotate"
            axisLabel="Y"
            mode="rotate"
            scale={ROTATE_DEG_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeRotatePreview({
                  targetId: activeTargetId,
                  axis: "y",
                  rawDegrees: v,
                  snap: { enabled: snapEnabled, step_degrees: snapStepDegrees },
                })
              );
            }}
            onCommit={(deg) => {
              clearGizmoPreview();
              commitRotateFromDrag("y", deg);
            }}
          />
          <DragPad
            enabled={enabled}
            label="Rotate"
            axisLabel="Z"
            mode="rotate"
            scale={ROTATE_DEG_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeRotatePreview({
                  targetId: activeTargetId,
                  axis: "z",
                  rawDegrees: v,
                  snap: { enabled: snapEnabled, step_degrees: snapStepDegrees },
                })
              );
            }}
            onCommit={(deg) => {
              clearGizmoPreview();
              commitRotateFromDrag("z", deg);
            }}
          />
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-2">
          <DragPad
            enabled={enabled}
            label="Scale"
            axisLabel="Uniform"
            mode="scale"
            scale={SCALE_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeScalePreview({
                  targetId: activeTargetId,
                  axis: "uniform",
                  rawFactor: v,
                  snap: { enabled: snapEnabled, step_factor: snapStepFactor },
                })
              );
            }}
            onCommit={(factor) => {
              clearGizmoPreview();
              commitScaleFromDrag("uniform", factor);
            }}
          />
          <DragPad
            enabled={enabled}
            label="Scale"
            axisLabel="X"
            mode="scale"
            scale={SCALE_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeScalePreview({
                  targetId: activeTargetId,
                  axis: "x",
                  rawFactor: v,
                  snap: { enabled: snapEnabled, step_factor: snapStepFactor },
                })
              );
            }}
            onCommit={(factor) => {
              clearGizmoPreview();
              commitScaleFromDrag("x", factor);
            }}
          />
          <DragPad
            enabled={enabled}
            label="Scale"
            axisLabel="Y"
            mode="scale"
            scale={SCALE_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeScalePreview({
                  targetId: activeTargetId,
                  axis: "y",
                  rawFactor: v,
                  snap: { enabled: snapEnabled, step_factor: snapStepFactor },
                })
              );
            }}
            onCommit={(factor) => {
              clearGizmoPreview();
              commitScaleFromDrag("y", factor);
            }}
          />
          <DragPad
            enabled={enabled}
            label="Scale"
            axisLabel="Z"
            mode="scale"
            scale={SCALE_PER_PX}
            onPreview={(v) => {
              if (v == null) return clearGizmoPreview();
              setGizmoPreview(
                makeScalePreview({
                  targetId: activeTargetId,
                  axis: "z",
                  rawFactor: v,
                  snap: { enabled: snapEnabled, step_factor: snapStepFactor },
                })
              );
            }}
            onCommit={(factor) => {
              clearGizmoPreview();
              commitScaleFromDrag("z", factor);
            }}
          />
        </div>
      )}

      <div className="text-xs opacity-70">
        UI-only: drag previews with a ghost; release emits one governed tool payload.
      </div>
    </div>
  );
}

