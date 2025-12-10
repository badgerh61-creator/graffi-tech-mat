import React from "react";
import UIPanel from "./UIPanel";
import { useModelTransformStore } from "../store/modelTransformStore";

export default function ModelTransformPanel() {
  const { position, rotation, scale, setPosition, setRotation, setScale, reset } =
    useModelTransformStore();

  return (
    <UIPanel title="Transform">
      <div className="space-y-4 text-sm">

        {/* POSITION */}
        <div>
          <label className="text-xs font-medium">Position</label>
          <div className="grid grid-cols-3 gap-2 mt-1">
            <input type="number" className="input-xs"
              value={position.x}
              onChange={(e) => setPosition("x", e.target.value)}
            />
            <input type="number" className="input-xs"
              value={position.y}
              onChange={(e) => setPosition("y", e.target.value)}
            />
            <input type="number" className="input-xs"
              value={position.z}
              onChange={(e) => setPosition("z", e.target.value)}
            />
          </div>
        </div>

        {/* ROTATION */}
        <div>
          <label className="text-xs font-medium">Rotation</label>
          <div className="grid grid-cols-3 gap-2 mt-1">
            <input type="number" className="input-xs"
              value={rotation.x}
              onChange={(e) => setRotation("x", e.target.value)}
            />
            <input type="number" className="input-xs"
              value={rotation.y}
              onChange={(e) => setRotation("y", e.target.value)}
            />
            <input type="number" className="input-xs"
              value={rotation.z}
              onChange={(e) => setRotation("z", e.target.value)}
            />
          </div>
        </div>

        {/* SCALE */}
        <div>
          <label className="text-xs font-medium">Scale</label>
          <input
            type="range"
            className="w-full"
            min="0.1"
            max="5"
            step="0.01"
            value={scale}
            onChange={(e) => setScale(e.target.value)}
          />
        </div>

        <button className="btn-sm w-full" onClick={reset}>
          Reset Transform
        </button>

      </div>
    </UIPanel>
  );
}
