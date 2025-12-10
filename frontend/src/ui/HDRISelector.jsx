import React from "react";
import { motion } from "framer-motion";
import { useUIStore } from "../store/uiStore";

const BUILT_INS = [
  { id: "studio", name: "Studio", preset: "studio" },
  { id: "outdoor", name: "Outdoor", preset: "sunset" },
  { id: "cinema", name: "Cinematic", preset: "city" },
  { id: "product", name: "Product", preset: "lobby" },
];

export default function HDRISelector() {
  const hdr = useUIStore((s) => s.hdr);
  const setHDRI = useUIStore((s) => s.setHDRI);
  const setHDRRotation = useUIStore((s) => s.setHDRRotation);
  const setHDRIntensity = useUIStore((s) => s.setHDRIntensity);

  function handleUpload(e) {
    const f = e.target.files?.[0];
    if (!f) return;
    const url = URL.createObjectURL(f);
    setHDRI({ type: "file", url, id: "custom" });
  }

  return (
    <div className="p-3">
      <div className="text-sm font-medium mb-2">Environment</div>

      {/* Built-in presets */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        {BUILT_INS.map((b) => (
          <motion.button
            key={b.id}
            whileHover={{ scale: 1.03 }}
            onClick={() =>
              setHDRI({ type: "preset", preset: b.preset, id: b.id })
            }
            className={`p-2 rounded border ${
              hdr.id === b.id
                ? "border-indigo-500 bg-indigo-50"
                : "bg-ui-surface"
            }`}
          >
            <div className="h-16 flex items-center justify-center bg-slate-100 rounded text-xs">
              {b.name}
            </div>
          </motion.button>
        ))}
      </div>

      {/* Upload HDR */}
      <div className="mb-3">
        <label className="text-xs text-slate-600">Upload HDRI</label>
        <input type="file" accept=".hdr,.exr,image/*" onChange={handleUpload} />
      </div>

      {/* Rotation */}
      <div className="mb-3">
        <label className="text-xs text-slate-600">Rotation</label>
        <input
          type="range"
          min={0}
          max={360}
          value={hdr.rotation}
          onChange={(e) => setHDRRotation(Number(e.target.value))}
        />
      </div>

      {/* Intensity */}
      <div>
        <label className="text-xs text-slate-600">Intensity</label>
        <input
          type="range"
          min={0}
          max={3}
          step={0.01}
          value={hdr.intensity}
          onChange={(e) => setHDRIntensity(Number(e.target.value))}
        />
      </div>
    </div>
  );
}
