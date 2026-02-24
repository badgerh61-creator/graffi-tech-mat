import React, { useMemo, useState } from "react";
import { executeTool } from "../../services/studio/toolExecutionAdapter";
import { useSelection } from "../selection/selectionStore";
import { toolPreflightGuard } from "../tools/toolPreflightGuard";

/**
 * Tier 7.14
 * - Uses selectionStore (v2 primary) + preflight guard
 * - Blocks execution with normalized reasons (no_selection/no_snapshot/ui_disabled)
 * - Executes only via canonical adapter (Tier 7.12)
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

  const reasonText = useMemo(() => {
    if (preflight.ok) return null;
    if (preflight.reason === "no_selection") return "select a target";
    if (preflight.reason === "no_snapshot") return "no active snapshot";
    if (preflight.reason === "ui_disabled") return "disabled";
    return "blocked";
  }, [preflight]);

  const canSubmit = useMemo(() => {
    return preflight.ok && !busy;
  }, [preflight, busy]);

  async function execute() {
    if (!preflight.ok || busy) return;

    setBusy(true);
    setLastError(null);

    const tool =
      operation === "translate"
        ? "TRANSLATE"
        : operation === "rotate"
        ? "ROTATE"
        : "SCALE";

    const payload =
      operation === "scale"
        ? { target_id: preflight.target_id, factor: Number(factor) }
        : operation === "rotate"
        ? { target_id: preflight.target_id, degrees: Number(degrees), axis: "y" } // axis stub
        : {
            target_id: preflight.target_id,
            x: Number(x),
            y: Number(y),
            z: Number(z),
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
        <div className="text-sm font-semibold">Transform (Tier 7.14)</div>
        <div className="text-xs opacity-75">
          Target: {preflight.ok ? preflight.target_id : "none"}
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
        onChange={(e) => setValue(e.target.value)}
        disabled={disabled}
      />
    </div>
  );
}
