// frontend/src/editor/toolbar/ToolContextBar.jsx

import React, { useMemo } from "react";
import { useSelection } from "../selection/selectionStore";
import { useGizmoMode, setGizmoMode } from "../gizmo/gizmoModeStore";
import {
  useSnap,
  setSnapEnabled,
  setSnapMode,
  setGridSize,
} from "../transform/snapStore";

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

// ✅ Tier 7.58 — constraint violations
import { useConstraintViolations } from "../constraints/constraintViolationStore";

// ✅ Tier 7.66 — history
import {
  useHistory,
  historyUndo,
  historyRedo,
  historyCanUndo,
  historyCanRedo,
} from "../history/historyStore";

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

export default function ToolContextBar({
  canEdit,
  reasons,
  lockLabelText,
  onRestoreSnapshot, // ✅ required for undo/redo
}) {
  const { selectedId } = useSelection();
  const mode = useGizmoMode().mode;
  const snap = useSnap();

  // ✅ Tier 7.64
  const transformSpace = useTransformSpace().mode;

  // ✅ Tier 7.41
  const filter = useSelectionFilter().filter;

  // ✅ Tier 7.58
  const { violations } = useConstraintViolations();

  // ✅ Tier 7.66
  const history = useHistory();

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

      {/* SNAP SYSTEM (Tier 7.65 upgraded) */}
      <div className="flex items-center gap-2 ml-3 border-l pl-2">
        {/* Enable */}
        <label className="flex items-center gap-1 text-sm">
          <input
            type="checkbox"
            disabled={!canEdit}
            checked={!!snap.enabled}
            onChange={(e) => setSnapEnabled(e.target.checked)}
          />
          Snap
        </label>

        {/* Mode */}
        <select
          className="border rounded px-2 py-1 text-xs"
          value={snap.mode}
          disabled={!canEdit}
          onChange={(e) => setSnapMode(e.target.value)}
        >
          <option value="none">None</option>
          <option value="grid">Grid</option>
          <option value="surface">Surface</option>
          <option value="object">Object</option>
        </select>

        {/* Grid Size */}
        {snap.mode === "grid" && (
          <input
            className="border rounded px-2 py-1 w-16 text-xs"
            type="number"
            step="0.1"
            value={snap.gridSize}
            disabled={!canEdit}
            onChange={(e) => setGridSize(Number(e.target.value || 1))}
          />
        )}

        {/* Legacy precision snap (kept for compatibility) */}
        <div className="text-xs opacity-70">
          Move:
          <input
            className="border rounded px-2 py-1 w-16 ml-1"
            type="number"
            step="0.01"
            disabled={!canEdit || !snap.enabled}
            value={snap.step ?? 0.1}
            onChange={(e) =>
              setSnap({ step: Number(e.target.value || 0.1) })
            }
          />
        </div>

        <div className="text-xs opacity-70">
          Rot:
          <input
            className="border rounded px-2 py-1 w-16 ml-1"
            type="number"
            step="1"
            disabled={!canEdit || !snap.enabled}
            value={snap.step_degrees ?? 5}
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

      {/* ✅ Undo / Redo (Tier 7.66) */}
      <div className="flex items-center gap-2 ml-3 border-l pl-2">
        <button
          className="border rounded px-2 py-1 text-xs"
          disabled={!historyCanUndo()}
          onClick={() => {
            const snap = historyUndo();
            if (snap?.id) {
              onRestoreSnapshot?.(snap.id);
            }
          }}
        >
          Undo
        </button>

        <button
          className="border rounded px-2 py-1 text-xs"
          disabled={!historyCanRedo()}
          onClick={() => {
            const snap = historyRedo();
            if (snap?.id) {
              onRestoreSnapshot?.(snap.id);
            }
          }}
        >
          Redo
        </button>
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

      {/* ✅ Tier 7.67 — Keyboard shortcuts hint */}
      <div className="w-full text-[11px] opacity-60 border-t pt-1 mt-1">
        G: Move · R: Rotate · S: Scale · Ctrl+Z: Undo · Ctrl+Shift+Z: Redo · Ctrl+D: Duplicate · Esc: Clear
      </div>
    </div>
  );
}
