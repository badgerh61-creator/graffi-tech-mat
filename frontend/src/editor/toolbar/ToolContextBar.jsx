// frontend/src/editor/toolbar/ToolContextBar.jsx
import React, { useMemo } from "react";
import { useSelection } from "../selection/selectionStore";
import { useGizmoMode, setGizmoMode } from "../gizmo/gizmoModeStore";
import { useSnap, setSnap } from "../transform/snapStore";

// ✅ Tier 7.41 — selection filter dropdown
import {
  useSelectionFilter,
  setSelectionFilter,
} from "../selection/selectionFilterStore";

// ✅ Tier 7.58 — canonical constraint violation indicator
import { useConstraintViolations } from "../constraints/constraintViolationStore";

function Button({ onClick, disabled, active, children, title }) {
  const cls = active
    ? "border rounded px-2 py-1 text-sm bg-gray-100"
    : "border rounded px-2 py-1 text-sm";
  return (
    <button className={cls} onClick={onClick} disabled={disabled} title={title}>
      {children}
    </button>
  );
}

function ReasonPills({ reasons }) {
  if (!reasons?.length) return null;
  return (
    <div className="flex flex-wrap gap-1">
      {reasons.map((r) => (
        <span key={r} className="border rounded px-2 py-0.5 text-xs bg-red-50">
          {r}
        </span>
      ))}
    </div>
  );
}

/**
 * Props:
 * - canEdit: boolean
 * - reasons: string[] (7.36 stable order)
 * - lockLabelText: string (optional)
 */
export default function ToolContextBar({ canEdit, reasons, lockLabelText }) {
  const { selectedId } = useSelection();
  const mode = useGizmoMode().mode;
  const snap = useSnap().snap;

  // ✅ Tier 7.41
  const filter = useSelectionFilter().filter;

  // ✅ Tier 7.58
  const { violations } = useConstraintViolations();

  const selectionShort = useMemo(() => {
    if (!selectedId) return "none";
    const parts = String(selectedId).split("::");
    return parts[0] + (parts[1] ? " :: " + parts[1] : "");
  }, [selectedId]);

  return (
    <div className="border rounded p-2 flex items-center gap-2 flex-wrap">
      <div className="text-sm font-semibold">Tool</div>

      <div className="text-xs opacity-70">
        Selection: <span className="font-mono">{selectionShort}</span>
      </div>

      <div className="flex items-center gap-2 ml-2">
        <div className="text-xs opacity-70">Select</div>
        <select
          className="border rounded px-2 py-1 text-sm"
          value={filter}
          onChange={(e) => setSelectionFilter(e.target.value)}
          title="Selection Filter"
        >
          <option value="all">All</option>
          <option value="objects">Objects</option>
          <option value="meshes">Meshes</option>
          <option value="decals">Decals</option>
        </select>
      </div>

      <div className="flex items-center gap-1 ml-2">
        <Button
          disabled={!canEdit}
          active={mode === "translate"}
          onClick={() => setGizmoMode("translate")}
          title="Translate (G)"
        >
          Move
        </Button>
        <Button
          disabled={!canEdit}
          active={mode === "rotate"}
          onClick={() => setGizmoMode("rotate")}
          title="Rotate (R)"
        >
          Rotate
        </Button>
        <Button
          disabled={!canEdit}
          active={mode === "scale"}
          onClick={() => setGizmoMode("scale")}
          title="Scale (S)"
        >
          Scale
        </Button>
      </div>

      <div className="flex items-center gap-2 ml-3">
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            disabled={!canEdit}
            checked={!!snap.enabled}
            onChange={(e) => setSnap({ enabled: e.target.checked })}
          />
          Snap
        </label>

        <div className="text-xs opacity-70">
          Move:
          <input
            className="border rounded px-2 py-1 w-20 ml-1"
            type="number"
            step="0.01"
            disabled={!canEdit || !snap.enabled}
            value={snap.step}
            onChange={(e) => setSnap({ step: Number(e.target.value || 0.1) })}
          />
        </div>

        <div className="text-xs opacity-70">
          Rotate:
          <input
            className="border rounded px-2 py-1 w-20 ml-1"
            type="number"
            step="1"
            disabled={!canEdit || !snap.enabled}
            value={snap.step_degrees}
            onChange={(e) =>
              setSnap({ step_degrees: Number(e.target.value || 5) })
            }
          />
        </div>

        <div className="text-xs opacity-70">
          Scale:
          <input
            className="border rounded px-2 py-1 w-20 ml-1"
            type="number"
            step="0.01"
            disabled={!canEdit || !snap.enabled}
            value={snap.step_factor}
            onChange={(e) =>
              setSnap({ step_factor: Number(e.target.value || 0.1) })
            }
          />
        </div>
      </div>

      <div className="flex items-center gap-1 ml-3">
        <span className="text-xs opacity-70">Axis</span>
        {["none", "x", "y", "z"].map((axis) => {
          const active = snap.axis_lock === axis;
          return (
            <button
              key={axis}
              className={
                active
                  ? "border rounded px-2 py-1 text-xs bg-gray-100"
                  : "border rounded px-2 py-1 text-xs"
              }
              disabled={!canEdit}
              onClick={() => setSnap({ axis_lock: axis })}
              title={`Axis lock ${axis.toUpperCase()}`}
            >
              {axis.toUpperCase()}
            </button>
          );
        })}
      </div>

      <div className="flex items-center gap-2 ml-3">
        <span className="text-xs opacity-70">Space</span>
        <select
          className="border rounded px-2 py-1 text-sm"
          disabled={!canEdit}
          value={snap.orientation}
          onChange={(e) => setSnap({ orientation: e.target.value })}
          title="Transform Orientation"
        >
          <option value="local">Local</option>
          <option value="world">World</option>
        </select>
      </div>

      {violations?.length ? (
        <div className="text-xs border rounded px-2 py-1 bg-red-50 ml-3">
          Constraints: {violations.length}
        </div>
      ) : null}

      <div className="flex-1" />

      {!canEdit ? (
        <div className="flex items-center gap-2">
          <span className="text-xs opacity-70">Editing blocked</span>
          <ReasonPills reasons={reasons} />
        </div>
      ) : (
        <div className="text-xs opacity-70">
          {lockLabelText || "Editing enabled"}
        </div>
      )}
    </div>
  );
}
