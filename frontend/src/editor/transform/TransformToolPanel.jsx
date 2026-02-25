// frontend/src/editor/transform/TransformToolPanel.jsx
import React, { useMemo, useState } from "react";
import { executeTool } from "../../services/studio/toolExecutionAdapter";
import { useSelection } from "../selection/selectionStore";
import { toolPreflightGuard } from "../tools/toolPreflightGuard";
import { buildSelectedTargetIds } from "../selection/buildSelectedTargetIds";
import { computeSelectionBboxStub } from "../selection/computeSelectionBboxStub"; // ✅ Tier 7.21
import PivotControls from "./PivotControls";
import { validatePivot } from "./validatePivot"; // ✅ Tier 7.23

// ✅ Tier 7.24
import SnapControls from "./SnapControls";
import { validateSnap } from "./validateSnap";

/**
 * Tier 7.14 + Tier 7.19 + Tier 7.20 + Tier 7.21 + Tier 7.23 + Tier 7.24
 * - Uses unified selectionStore (v2 primary/secondary) + preflight guard
 * - Blocks execution with normalized reasons (no_selection/no_snapshot/ui_disabled)
 * - Executes only via canonical adapter (Tier 7.12)
 * - Tier 7.19: adds selected_target_ids when multi-select
 * - Tier 7.20: adds pivot UI + pivot_mode/pivot binding when multi-select
 * - Tier 7.21: adds selection_bbox metadata when multi-select (deterministic stub)
 * - Tier 7.23: validates custom pivot (finite xyz) and blocks before hitting kernel
 * - Tier 7.24: shared SnapControls + canonical snap payload shapes + UI validation
 */
export default function TransformToolPanel({
  activeSnapshot,
  disabled = false,
  onExecuted,
}) {
  const selection = useSelection();

  const [operation, setOperation] = useState("translate");
  const [x, setX] = useState(0);
  const [y, setY] = useState(0);
  const [z, setZ] = useState(0);
  const [factor, setFactor] = useState(1.0);
  const [degrees, setDegrees] = useState(5);

  // Tier 7.20 pivot UI state
  const [pivotMode, setPivotMode] = useState("bbox_center");
  const [customPivot, setCustomPivot] = useState({ x: 0, y: 0, z: 0 });

  // ✅ Tier 7.24 snapping state
  const [snapEnabled, setSnapEnabled] = useState(true);
  const [snapStepTranslate, setSnapStepTranslate] = useState(0.25);
  const [snapStepDegrees, setSnapStepDegrees] = useState(5);
  const [snapStepFactor, setSnapStepFactor] = useState(0.05);

  const [busy, setBusy] = useState(false);
  const [lastError, setLastError] = useState(null);

  const preflight = useMemo(
    () =>
      toolPreflightGuard({
        selection,
        uiDisabled: disabled,
        activeSnapshotId: activeSnapshot?.id,
      }),
    [selection, disabled, activeSnapshot?.id]
  );

  const selectedIds = useMemo(
    () => buildSelectedTargetIds(selection),
    [selection]
  );

  const isMulti = preflight.ok && selectedIds.length > 1;
  const showPivot = isMulti;

  // ✅ Tier 7.21 selection bbox metadata (deterministic stub)
  const selectionBbox = useMemo(
    () => (isMulti ? computeSelectionBboxStub(selectedIds) : null),
    [isMulti, selectedIds]
  );

  // ✅ Tier 7.23 pivot validation (only matters when multi + custom)
  const pivotValidation = useMemo(
    () => (isMulti ? validatePivot(pivotMode, customPivot) : { ok: true }),
    [isMulti, pivotMode, customPivot]
  );

  // ✅ Tier 7.24 snap validation (operation-specific)
  const snapValidation = useMemo(() => {
    if (!snapEnabled) return { ok: true };
    if (operation === "rotate") return validateSnap(true, snapStepDegrees);
    if (operation === "scale") return validateSnap(true, snapStepFactor);
    return validateSnap(true, snapStepTranslate);
  }, [snapEnabled, operation, snapStepTranslate, snapStepDegrees, snapStepFactor]);

  const reasonText = useMemo(() => {
    if (!preflight.ok) {
      if (preflight.reason === "no_selection") return "select a target";
      if (preflight.reason === "no_snapshot") return "no active snapshot";
      if (preflight.reason === "ui_disabled") return "disabled";
      return "blocked";
    }
    if (isMulti && !pivotValidation.ok) return "invalid_pivot";
    if (!snapValidation.ok) return snapValidation.reason;
    return null;
  }, [preflight, isMulti, pivotValidation, snapValidation]);

  const canSubmit = useMemo(() => {
    if (!preflight.ok) return false;
    if (busy) return false;
    if (isMulti && !pivotValidation.ok) return false;
    if (!snapValidation.ok) return false;
    return true;
  }, [preflight, busy, isMulti, pivotValidation, snapValidation]);

  async function execute() {
    if (!preflight.ok || busy) return;

    if (isMulti && !pivotValidation.ok) {
      setLastError("invalid_pivot");
      return;
    }

    if (!snapValidation.ok) {
      setLastError(snapValidation.reason);
      return;
    }

    setBusy(true);
    setLastError(null);

    const tool =
      operation === "translate"
        ? "TRANSLATE"
        : operation === "rotate"
        ? "ROTATE"
        : "SCALE";

    const base = {
      target_id: preflight.target_id,

      // ✅ Tier 7.19 → Tier 7.5 multiselect fields
      selected_target_ids: isMulti ? selectedIds : undefined,

      // ✅ Tier 7.20 pivot fields
      pivot_mode: isMulti ? pivotMode : undefined,
      pivot: isMulti && pivotMode === "custom" ? customPivot : undefined,

      // ✅ Tier 7.21 bbox metadata
      selection_bbox: isMulti && selectionBbox ? selectionBbox : undefined,

      // optional metadata (useful for audit/telemetry)
      drag_source: "nudge",
    };

    // ✅ Tier 7.24 canonical snap shape
    const snap =
      operation === "rotate"
        ? { enabled: snapEnabled, step_degrees: Number(snapStepDegrees) }
        : operation === "scale"
        ? { enabled: snapEnabled, step_factor: Number(snapStepFactor) }
        : { enabled: snapEnabled, step: Number(snapStepTranslate) };

    const payload =
      operation === "scale"
        ? { ...base, factor: Number(factor), snap }
        : operation === "rotate"
        ? { ...base, degrees: Number(degrees), axis: "y", snap } // axis stub
        : {
            ...base,
            x: Number(x),
            y: Number(y),
            z: Number(z),
            snap,
          };

    try {
      const res = await executeTool({
        snapshotId: activeSnapshot.id,
        station: "geometry",
        tool,
        payload,
        mode: "proposals", // ✅ canonical governed path
        enablePreview: false,
      });

      if (!res.ok) {
        throw new Error(
          res.error?.detail || `Tool rejected (${res.error?.kind || "error"})`
        );
      }

      onExecuted?.(res.data);
    } catch (e) {
      setLastError(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">
          Transform (Tier 7.14 + 7.19 + 7.20 + 7.21 + 7.23 + 7.24)
        </div>
        <div className="text-xs opacity-75">
          Target: {preflight.ok ? preflight.target_id : "none"}{" "}
          {preflight.ok ? `(selected ${selectedIds.length})` : ""}
        </div>
      </div>

      <div className="flex gap-2 items-center">
        <label className="text-xs opacity-70">Operation</label>
        <select
          className="border rounded px-2 py-1 text-sm"
          value={operation}
          onChange={(e) => setOperation(e.target.value)}
          disabled={disabled || busy}
        >
          <option value="translate">Translate</option>
          <option value="rotate">Rotate</option>
          <option value="scale">Scale</option>
        </select>
      </div>

      {operation === "translate" ? (
        <div className="grid grid-cols-3 gap-2">
          <Field label="X" value={x} setValue={setX} disabled={disabled || busy} />
          <Field label="Y" value={y} setValue={setY} disabled={disabled || busy} />
          <Field label="Z" value={z} setValue={setZ} disabled={disabled || busy} />
        </div>
      ) : operation === "rotate" ? (
        <div className="grid grid-cols-1 gap-2">
          <Field
            label="Degrees"
            value={degrees}
            setValue={setDegrees}
            disabled={disabled || busy}
          />
          <div className="text-xs opacity-70">
            Axis is stubbed to "y" for now; Tier 7.7+7.4 axis locks/gizmo handles will drive this.
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-2">
          <Field
            label="Factor"
            value={factor}
            setValue={setFactor}
            disabled={disabled || busy}
          />
        </div>
      )}

      {/* ✅ Tier 7.20: Pivot controls only when multi-select */}
      {showPivot ? (
        <div className="space-y-2">
          <PivotControls
            pivotMode={pivotMode}
            setPivotMode={setPivotMode}
            customPivot={customPivot}
            setCustomPivot={setCustomPivot}
            disabled={!preflight.ok || busy || disabled}
          />
          {!pivotValidation.ok ? (
            <div className="text-xs opacity-80 border rounded p-2">
              Pivot invalid: enter finite X/Y/Z values.
            </div>
          ) : null}
        </div>
      ) : null}

      {/* ✅ Tier 7.24: Snap controls (shared) */}
      <SnapControls
        enabled={snapEnabled}
        setEnabled={setSnapEnabled}
        step={
          operation === "rotate"
            ? snapStepDegrees
            : operation === "scale"
            ? snapStepFactor
            : snapStepTranslate
        }
        setStep={(v) => {
          if (operation === "rotate") setSnapStepDegrees(v);
          else if (operation === "scale") setSnapStepFactor(v);
          else setSnapStepTranslate(v);
        }}
        label="Snapping"
        stepLabel={
          operation === "rotate"
            ? "Degrees step"
            : operation === "scale"
            ? "Factor step"
            : "Grid step"
        }
        stepInputStep={operation === "rotate" ? 1 : 0.05}
        disabled={!preflight.ok || busy || disabled}
      />

      {!snapValidation.ok ? (
        <div className="text-xs opacity-80 border rounded p-2">
          Snap invalid: step must be a finite number &gt; 0 when enabled.
        </div>
      ) : null}

      {lastError ? (
        <div className="text-xs border rounded p-2">
          <div className="font-semibold">Rejected</div>
          <div className="opacity-80">{lastError}</div>
        </div>
      ) : null}

      <button
        data-testid="transform-execute"
        className="border rounded px-3 py-2 text-sm"
        onClick={execute}
        disabled={!canSubmit}
        title={reasonText ?? ""}
      >
        {busy ? "Executing..." : canSubmit ? "Execute" : `Blocked: ${reasonText}`}
      </button>

      <div className="text-xs opacity-70">
        Preflight blocks missing selection/snapshot/disabled state before hitting the kernel.
        {isMulti ? " Multi-select payload + pivot + bbox metadata enabled." : ""}
      </div>
    </div>
  );
}

function Field({ label, value, setValue, disabled }) {
  return (
    <div className="space-y-1">
      <div className="text-xs opacity-70">{label}</div>
      <input
        className="border rounded px-2 py-1 text-sm w-full"
        type="number"
        value={value}
        onChange={(e) => setValue(Number(e.target.value))}
        disabled={disabled}
      />
    </div>
  );
}
