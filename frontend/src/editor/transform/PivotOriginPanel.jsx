import React from "react";
import { useEffect, useState } from "react";
import { useSelection } from "../selection/selectionStore";
import { setPivotPreview, clearPivotPreview } from "./pivotPreviewStore";

export default function PivotOriginPanel({
  snapshot,
  canEdit,
  onCommitTool,
  onRequestPivotPreset,
}) {
  const { selectedId } = useSelection();
  const objectId = selectedId ? String(selectedId).split("::")[0] : null;
  const objects = snapshot?.body_state?.objects || [];
  const obj = objects.find((o) => String(o.id) === String(objectId)) || null;
  const pivot = obj?.pivot || null;

  const [x, setX] = useState(0);
  const [y, setY] = useState(0);
  const [z, setZ] = useState(0);

  useEffect(() => {
    setX(Number(pivot?.x || 0));
    setY(Number(pivot?.y || 0));
    setZ(Number(pivot?.z || 0));
  }, [pivot?.x, pivot?.y, pivot?.z, objectId]);

  function preview(next) {
    if (!objectId) return;
    setPivotPreview({
      object_id: objectId,
      pivot: next,
    });
  }

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Pivot / Origin</div>

      <div className="text-xs opacity-70">
        Target: <span className="font-mono">{objectId || "none"}</span>
      </div>

      <div className="grid grid-cols-3 gap-2">
        <label className="text-xs">
          X
          <input
            className="border rounded px-2 py-1 w-full"
            type="number"
            step="0.01"
            value={x}
            onChange={(e) => {
              const v = Number(e.target.value || 0);
              setX(v);
              preview({ x: v, y, z });
            }}
          />
        </label>

        <label className="text-xs">
          Y
          <input
            className="border rounded px-2 py-1 w-full"
            type="number"
            step="0.01"
            value={y}
            onChange={(e) => {
              const v = Number(e.target.value || 0);
              setY(v);
              preview({ x, y: v, z });
            }}
          />
        </label>

        <label className="text-xs">
          Z
          <input
            className="border rounded px-2 py-1 w-full"
            type="number"
            step="0.01"
            value={z}
            onChange={(e) => {
              const v = Number(e.target.value || 0);
              setZ(v);
              preview({ x, y, z: v });
            }}
          />
        </label>
      </div>

      <div className="flex items-center gap-2 flex-wrap">
        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !objectId}
          onClick={() =>
            onCommitTool?.({
              tool: "SCENE_SET_OBJECT_PIVOT",
              station: "geometry",
              payload: {
                object_id: objectId,
                pivot: { x, y, z },
              },
            })
          }
        >
          Apply Pivot
        </button>

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !objectId}
          onClick={() => {
            clearPivotPreview();
            onCommitTool?.({
              tool: "SCENE_RESET_OBJECT_PIVOT",
              station: "geometry",
              payload: { object_id: objectId },
            });
          }}
        >
          Reset Pivot
        </button>

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !objectId}
          onClick={() => onRequestPivotPreset?.("center", objectId)}
        >
          Center Pivot
        </button>

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !objectId}
          onClick={() => onRequestPivotPreset?.("bounds_bottom_center", objectId)}
        >
          Bottom Center
        </button>
      </div>

      <div className="text-[11px] opacity-60">
        Tier 7.61 edits transform origin only. No mesh rebake occurs.
      </div>
    </div>
  );
}
