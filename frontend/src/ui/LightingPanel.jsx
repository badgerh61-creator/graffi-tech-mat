import React from "react";
import UIPanel from "./UIPanel";
import { useUIStore } from "../store/uiStore";

export default function LightingPanel() {
  const hdr = useUIStore((s) => s.hdr);
  const setHDRIntensity = useUIStore((s) => s.setHDRIntensity);
  const setAmbient = useUIStore((s) => s.setAmbient);
  const setDirLight = useUIStore((s) => s.setDirectional);
  const toggleShadows = useUIStore((s) => s.toggleShadows);

  return (
    <UIPanel title="Lighting">
      <div className="space-y-3 text-sm">

        {/* Ambient Light */}
        <div>
          <label className="text-xs">Ambient Intensity</label>
          <input
            type="range"
            min="0"
            max="2"
            step="0.01"
            onChange={(e) => setAmbient(Number(e.target.value))}
            className="w-full"
            value={hdr?.ambient ?? 0.6}
          />
        </div>

        {/* Directional Light */}
        <div>
          <label className="text-xs">Directional Intensity</label>
          <input
            type="range"
            min="0"
            max="3"
            step="0.01"
            onChange={(e) => setDirLight(Number(e.target.value))}
            className="w-full"
            value={hdr?.dirLight ?? 1.2}
          />
        </div>

        {/* HDRI Intensity */}
        <div>
          <label className="text-xs">HDRI Intensity</label>
          <input
            type="range"
            min="0"
            max="5"
            step="0.05"
            onChange={(e) => setHDRIntensity(Number(e.target.value))}
            className="w-full"
            value={hdr?.intensity ?? 1.0}
          />
        </div>

        {/* Shadows */}
        <div className="flex items-center gap-2">
          <label className="text-xs">Shadows</label>
          <input
            type="checkbox"
            onChange={toggleShadows}
            checked={hdr?.shadows ?? true}
          />
        </div>

      </div>
    </UIPanel>
  );
}
