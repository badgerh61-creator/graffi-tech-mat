import React, { useMemo, useState } from "react";
import { useSelection } from "../selection/selectionStore";
import { executeTool } from "../../services/studio/toolExecutionAdapter";

/**
 * Tier 7.11 + 7.12
 * - target_id binds from selectionStore.selectedId
 * - tool execution goes through the canonical adapter (no direct fetch)
 */
export default function TransformToolPanel({
  activeSnapshot,
  disabled = false,
  onExecuted,
}) {
  const { selectedId } = useSelection();

  const [operation, setOperation] = useState("translate");
  const [x, setX] = useState(0);
  const [y, setY] = useState(0);
  const [z, setZ] = useState(0);
  const [factor, setFactor] = useState(1.0);
  const [degrees, setDegrees] = useState(5);

  const [busy, setBusy] = useState(false);
  const [lastError, setLastError] = useState(null);

  const canSubmit = useMemo(() => {
    if (disabled) return false;
    if (!activeSnapshot?.id) return false;
    if (!selectedId) return false;
    return true;
  }, [disabled, activeSnapshot, selectedId]);

  const reasonDisabled = useMemo(() => {
    if (disabled) return "disabled";
    if (!activeSnapshot?.id) return "no active snapshot";
    if (!selectedId) return "select a target";
    return null;
  }, [disabled, activeSnapshot, selectedId]);

  async function execute() {
    if (!canSubmit) return;

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
        ? { target_id: selectedId, factor: Number(factor) }
        : operation === "rotate"
        ? { target_id: selectedId, degrees: Number(degrees), axis: "y" } // axis stub
        : { target_id: selectedId, x: Number(x), y: Number(y), z: Number(z) };

    try {
      const res = await executeTool({
        snapshotId: activeSnapshot.id,
        station: "geometry",
        tool,
        payload,
        mode: "proposals",      // ✅ canonical governed path
        enablePreview: false,   // set true only if /assistant/proposals/preview exists
      });

      if (!res.ok) {
        throw new Error(res.error?.detail || `Tool rejected (${res.error?.kind || "error"})`);
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
        <div className="text-sm font-semibold">Transform (Tier 7.11)</div>
        <div className="text-xs opacity-75">
          Target: {selectedId ?? "none"}
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
          <Field label="Factor" value={factor} setValue={setFactor} disabled={disabled || busy} />
        </div>
      )}

      {lastError ? (
        <div className="text-xs border rounded p-2">
          <div className="font-semibold">Rejected</div>
          <div className="opacity-80">{lastError}</div>
        </div>
      ) : null}

      <button
        className="border rounded px-3 py-2 text-sm"
        onClick={execute}
        disabled={!canSubmit || busy}
        title={reasonDisabled ?? ""}
      >
        {busy ? "Executing..." : canSubmit ? "Execute" : `Blocked: ${reasonDisabled}`}
      </button>

      <div className="text-xs opacity-70">
        This panel only constructs payloads (target_id from selection). The kernel decides.
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
