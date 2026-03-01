import React, { useEffect, useMemo, useState } from "react";
import { useSelection } from "../selection/selectionStore";

function clamp01(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return 0;
  return Math.max(0, Math.min(1, x));
}

export default function PaintParamsPanel({ snapshot, canEdit, onCommitTool }) {
  const { selectedId } = useSelection();
  const overrides = snapshot?.decor_state?.material_overrides || {};

  const activeOverride = useMemo(() => {
    if (!selectedId) return null;
    const tid = String(selectedId);
    return overrides[tid] || null;
  }, [overrides, selectedId]);

  const params = activeOverride?.params || {};

  const [color, setColor] = useState(params.color || "#777777");
  const [roughness, setRoughness] = useState(params.roughness ?? 0.6);
  const [metalness, setMetalness] = useState(params.metalness ?? 0.0);
  const [opacity, setOpacity] = useState(params.opacity ?? 1.0);

  useEffect(() => {
    setColor(params.color || "#777777");
    setRoughness(params.roughness ?? 0.6);
    setMetalness(params.metalness ?? 0.0);
    setOpacity(params.opacity ?? 1.0);
  }, [selectedId, activeOverride?.preset]);

  const hasOverride = !!activeOverride;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Paint Params</div>

      <div className="text-xs opacity-70">
        Target: <span className="font-mono">{selectedId || "none"}</span>
      </div>

      {!hasOverride ? (
        <div className="text-xs opacity-70">
          No override for this target yet. Apply a preset first (Tier 7.42).
        </div>
      ) : (
        <>
          <div className="text-xs opacity-70">
            Base preset: <span className="font-mono">{activeOverride.preset}</span>
          </div>

          <label className="flex items-center justify-between gap-2 text-sm">
            <span>Color</span>
            <input
              className="border rounded px-2 py-1 w-36 font-mono"
              value={color}
              onChange={(e) => setColor(e.target.value)}
              placeholder="#RRGGBB"
              disabled={!canEdit}
            />
          </label>

          <label className="flex items-center justify-between gap-2 text-sm">
            <span>Roughness</span>
            <input
              className="border rounded px-2 py-1 w-24"
              type="number"
              step="0.05"
              value={roughness}
              onChange={(e) => setRoughness(clamp01(e.target.value))}
              disabled={!canEdit}
            />
          </label>

          <label className="flex items-center justify-between gap-2 text-sm">
            <span>Metalness</span>
            <input
              className="border rounded px-2 py-1 w-24"
              type="number"
              step="0.05"
              value={metalness}
              onChange={(e) => setMetalness(clamp01(e.target.value))}
              disabled={!canEdit}
            />
          </label>

          <label className="flex items-center justify-between gap-2 text-sm">
            <span>Opacity</span>
            <input
              className="border rounded px-2 py-1 w-24"
              type="number"
              step="0.05"
              value={opacity}
              onChange={(e) => setOpacity(clamp01(e.target.value))}
              disabled={!canEdit}
            />
          </label>

          <button
            className="border rounded px-3 py-2 text-sm"
            disabled={!canEdit}
            onClick={() =>
              onCommitTool?.({
                tool: "MATERIAL_UPDATE_PARAMS",
                station: "decor",
                payload: {
                  target_id: selectedId,
                  patch: { color, roughness, metalness, opacity },
                },
              })
            }
          >
            Commit Params
          </button>
        </>
      )}

      <div className="text-[11px] opacity-60">
        Params are clamped in apply. Color must be #RRGGBB.
      </div>
    </div>
  );
}
