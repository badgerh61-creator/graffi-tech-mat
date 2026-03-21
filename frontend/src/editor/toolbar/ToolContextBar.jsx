// frontend/src/editor/toolbar/ToolContextBar.jsx
import React, { useMemo } from "react";
import { useSelection } from "../selection/selectionStore";
import { useGizmoMode, setGizmoMode } from "../gizmo/gizmoModeStore";
import { useSnap, setSnap } from "../transform/snapStore";

// ✅ Tier 7.64 — transform space store
import {
  useTransformSpace,
  setTransformSpace,
} from "../transform/transformSpaceStore";

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

export default function ToolContextBar({ canEdit, reasons, lockLabelText }) {
  const { selectedId } = useSelection();
  const mode = useGizmoMode().mode;
  const snap = useSnap().snap;

  // ✅ Tier 7.64
  const transformSpace = useTransformSpace().mode;

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

      {/* Selection Filter */}
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

      {/* Gizmo */}
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

      {/* Transform Space */}
      <div className="flex items-center gap-1 ml-3">
        <span className="text-xs opacity-70">Space</span>
        {["world", "local", "pivot"].map((s) => {
          const active = transformSpace === s;
          return (
            <button
              key={s}
              className={
                active
                  ? "border rounded px-2 py-1 text-xs bg-gray-100"
                  : "border rounded px-2 py-1 text-xs"
              }
              disabled={!canEdit}
              onClick={() => setTransformSpace(s)}
            >
              {s.toUpperCase()}
            </button>
          );
        })}
      </div>

      {/* SNAP BLOCK (UPDATED) */}
      <div className="flex items-center gap-2 ml-3 border-l pl-2">
        {/* Enable */}
        <label className="flex items-center gap-1 text-sm">
          <input
            type="checkbox"
            disabled={!canEdit}
            checked={!!snap.enabled}
            onChange={(e) => setSnap({ enabled: e.target.checked })}
          />
          Snap
        </label>

        {/* NEW: Mode */}
        <select
          className="border rounded px-2 py-1 text-xs"
          value={snap.mode}
          disabled={!canEdit}
          onChange={(e) => setSnap({ mode: e.target.value })}
        >
          <option value="none">None</option>
          <option value="grid">Grid</option>
          <option value="surface">Surface</option>
          <option value="object">Object</option>
        </select>

        {/* NEW: Grid size */}
        {snap.mode === "grid" && (
          <input
            className="border rounded px-2 py-1 w-16 text-xs"
            type="number"
            step="0.1"
            value={snap.gridSize}
            disabled={!canEdit}
            onChange={(e) =>
              setSnap({ gridSize: Number(e.target.value || 1) })
            }
          />
        )}

        {/* Existing precision snap */}
        <div className="text-xs opacity-70">
          Move:
          <input
            className="border rounded px-2 py-1 w-16 ml-1"
            type="number"
            step="0.01"
            disabled={!canEdit || !snap.enabled}
            value={snap.step}
            onChange={(e) => setSnap({ step: Number(e.target.value || 0.1) })}
          />
        </div>

        <div className="text-xs opacity-70">
          Rot:
          <input
            className="border rounded px-2 py-1 w-16 ml-1"
            type="number"
            step="1"
            disabled={!canEdit || !snap.enabled}
            value={snap.step_degrees}
            onChange={(e) =>
              setSnap({ step_degrees: Number(e.target.value || 5) })
            }
          />
        </div>
      </div>

      {/* Axis Lock */}
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
            >
              {axis.toUpperCase()}
            </button>
          );
        })}
      </div>

      {/* Constraint indicator */}
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
