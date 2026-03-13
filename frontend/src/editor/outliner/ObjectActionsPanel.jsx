import React, { useState } from "react";
import { useSelection } from "../selection/selectionStore";

export default function ObjectActionsPanel({ canEdit, onCommitTool }) {
  const { selectedId } = useSelection();
  const objectId = selectedId ? String(selectedId).split("::")[0] : null;

  const [dx, setDx] = useState(1);
  const [dy, setDy] = useState(0);
  const [dz, setDz] = useState(0);

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Object Actions</div>

      <div className="text-xs opacity-70">
        Target: <span className="font-mono">{objectId || "none"}</span>
      </div>

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold opacity-80">Duplicate</div>

        <div className="grid grid-cols-3 gap-2">
          <label className="text-xs">
            X
            <input
              className="border rounded px-2 py-1 w-full"
              type="number"
              step="0.1"
              value={dx}
              onChange={(e) => setDx(Number(e.target.value || 0))}
            />
          </label>

          <label className="text-xs">
            Y
            <input
              className="border rounded px-2 py-1 w-full"
              type="number"
              step="0.1"
              value={dy}
              onChange={(e) => setDy(Number(e.target.value || 0))}
            />
          </label>

          <label className="text-xs">
            Z
            <input
              className="border rounded px-2 py-1 w-full"
              type="number"
              step="0.1"
              value={dz}
              onChange={(e) => setDz(Number(e.target.value || 0))}
            />
          </label>
        </div>

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !objectId}
          onClick={() =>
            onCommitTool?.({
              tool: "SCENE_DUPLICATE_OBJECT",
              station: "geometry",
              payload: {
                object_id: objectId,
                offset: { x: dx, y: dy, z: dz },
              },
            })
          }
        >
          Duplicate Object
        </button>
      </div>

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold opacity-80">Mirror</div>

        <div className="flex items-center gap-2">
          {["x", "y", "z"].map((axis) => (
            <button
              key={axis}
              className="border rounded px-3 py-2 text-sm"
              disabled={!canEdit || !objectId}
              onClick={() =>
                onCommitTool?.({
                  tool: "SCENE_MIRROR_OBJECT",
                  station: "geometry",
                  payload: {
                    object_id: objectId,
                    axis,
                  },
                })
              }
            >
              Mirror {axis.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      <div className="text-[11px] opacity-60">
        Duplicate and mirror create new scene objects. Source object is unchanged.
      </div>
    </div>
  );
}
