import React, { useEffect, useState } from "react";
import { useSelection } from "../selection/selectionStore";
import { useMultiSelection } from "../selection/multiSelectionStore";

export default function NumericTransformPanel({
  snapshot,
  canEdit,
  onCommitTool,
}) {
  const { selectedId } = useSelection();
  const { selectedIds } = useMultiSelection();

  const objectId = selectedId ? String(selectedId).split("::")[0] : null;

  const objects = snapshot?.body_state?.objects || [];
  const obj = objects.find((o) => String(o.id) === String(objectId)) || null;

  const t = obj?.transform || {};

  const [mode, setMode] = useState("absolute");

  const [pos, setPos] = useState({ x: 0, y: 0, z: 0 });
  const [rot, setRot] = useState({ x: 0, y: 0, z: 0 });
  const [scale, setScale] = useState({ x: 1, y: 1, z: 1 });

  useEffect(() => {
    if (!obj) return;

    setPos({
      x: Number(t?.pos?.x || 0),
      y: Number(t?.pos?.y || 0),
      z: Number(t?.pos?.z || 0),
    });

    setRot({
      x: Number(t?.rot?.x || 0),
      y: Number(t?.rot?.y || 0),
      z: Number(t?.rot?.z || 0),
    });

    setScale({
      x: Number(t?.scale?.x || 1),
      y: Number(t?.scale?.y || 1),
      z: Number(t?.scale?.z || 1),
    });
  }, [objectId]);

  if (!objectId) return null;

  function update(setter, axis, value) {
    const v = Number(value || 0);
    setter((prev) => ({ ...prev, [axis]: v }));
  }

  function applyAbsolute() {
    onCommitTool?.({
      tool: "SCENE_SET_OBJECT_TRANSFORM",
      station: "geometry",
      payload: {
        object_id: objectId,
        transform: {
          pos,
          rot,
          scale,
        },
      },
    });
  }

  function applyDelta() {
    onCommitTool?.({
      tool: "SCENE_BULK_OFFSET_TRANSFORM",
      station: "geometry",
      payload: {
        object_ids: selectedIds.length ? selectedIds : [objectId],
        delta: {
          pos,
          rot,
          scale,
        },
      },
    });
  }

  function Row({ label, values, setter }) {
    return (
      <div className="space-y-1">
        <div className="text-xs">{label}</div>
        <div className="grid grid-cols-3 gap-1">
          {["x", "y", "z"].map((axis) => (
            <input
              key={axis}
              className="border rounded px-1 py-1 text-xs"
              type="number"
              value={values[axis]}
              onChange={(e) => update(setter, axis, e.target.value)}
            />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="text-sm font-semibold">Numeric Transform</div>

      {/* MODE TOGGLE */}
      <div className="flex gap-2">
        <button
          className={`border rounded px-2 py-1 text-xs ${
            mode === "absolute" ? "bg-gray-100" : ""
          }`}
          onClick={() => setMode("absolute")}
        >
          Absolute
        </button>

        <button
          className={`border rounded px-2 py-1 text-xs ${
            mode === "delta" ? "bg-gray-100" : ""
          }`}
          onClick={() => setMode("delta")}
        >
          Delta
        </button>
      </div>

      <Row label="Position" values={pos} setter={setPos} />
      <Row label="Rotation" values={rot} setter={setRot} />
      <Row label="Scale" values={scale} setter={setScale} />

      {/* ACTION BUTTON */}
      <div className="flex gap-2">
        {mode === "absolute" ? (
          <button
            className="border rounded px-2 py-1 text-xs"
            disabled={!canEdit}
            onClick={applyAbsolute}
          >
            Apply Absolute
          </button>
        ) : (
          <button
            className="border rounded px-2 py-1 text-xs"
            disabled={!canEdit}
            onClick={applyDelta}
          >
            Apply Offset
          </button>
        )}
      </div>
    </div>
  );
}
