import React from "react";

export default function CameraToolbar({
  onFrameSelected,
  onFrameScene,
  onPreset,
}) {
  return (
    <div className="border rounded p-2 flex items-center gap-2 flex-wrap">
      <div className="text-sm font-semibold">Camera</div>

      <button className="border rounded px-2 py-1 text-sm" onClick={onFrameSelected}>
        Frame Selected
      </button>

      <button className="border rounded px-2 py-1 text-sm" onClick={onFrameScene}>
        Frame Scene
      </button>

      <div className="w-px h-5 bg-gray-300 mx-1" />

      <button className="border rounded px-2 py-1 text-sm" onClick={() => onPreset?.("front")}>
        Front
      </button>
      <button className="border rounded px-2 py-1 text-sm" onClick={() => onPreset?.("back")}>
        Back
      </button>
      <button className="border rounded px-2 py-1 text-sm" onClick={() => onPreset?.("left")}>
        Left
      </button>
      <button className="border rounded px-2 py-1 text-sm" onClick={() => onPreset?.("right")}>
        Right
      </button>
      <button className="border rounded px-2 py-1 text-sm" onClick={() => onPreset?.("top")}>
        Top
      </button>
      <button className="border rounded px-2 py-1 text-sm" onClick={() => onPreset?.("bottom")}>
        Bottom
      </button>
      <button className="border rounded px-2 py-1 text-sm" onClick={() => onPreset?.("iso")}>
        Iso
      </button>
    </div>
  );
}
