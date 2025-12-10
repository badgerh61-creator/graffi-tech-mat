// src/pages/Studio.jsx
import React, { useRef, useState, useCallback } from "react";

import SceneCanvas from "../engine/SceneCanvas";
import UIPanel from "../ui/UIPanel";
import ModelLibrary from "../ui/ModelLibrary";
import UploadPanel from "../widgets/UploadPanel";
import PresetCategories from "../ui/PresetCategories";
import PresetGallery from "../ui/PresetGallery";
import HDRISelector from "../ui/HDRISelector";

import { useMaterialStore } from "../store/materialStore";
import { useModelStore } from "../store/modelStore";
import { useHistoryStore } from "../store/historyStore";

import AppShortcuts from "../AppShortcuts";
import "../styles/index.css";

export default function Studio() {
  const sceneRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const material = useMaterialStore((s) => s.material);
  const setMaterial = useMaterialStore((s) => s.setMaterial);

  const addModelFromAsset = useModelStore((s) => s.addModelFromAsset);

  const pushHistory = useHistoryStore((s) => s.push);
  const undo = useHistoryStore((s) => s.undo);
  const redo = useHistoryStore((s) => s.redo);

  const handlePreset = useCallback(
    (name) => {
      if (!sceneRef.current) return;
      if (name === "front") sceneRef.current.setCameraPreset("front");
      if (name === "iso") sceneRef.current.setCameraPreset("iso");
      if (name === "reset") sceneRef.current.resetCamera();
    },
    [sceneRef]
  );

  // FIXED: Universal safe handler
  const onUploaded = (asset) => {
    addModelFromAsset(asset); // Will only add if model file
  };

  return (
    <div className="studio-page min-h-screen">
      <AppShortcuts undo={undo} redo={redo} />

      <div className="container mx-auto px-4 py-4">
        <h1 className="text-xl font-semibold mb-3">Graffi Studio — Ultra</h1>

        <div className="grid grid-cols-12 gap-4">
          {/* Canvas block */}
          <div className="col-span-9 bg-white rounded shadow-sm p-3">
            <div className="flex items-center justify-between mb-2">
              <div className="flex gap-2">
                <button className="btn-sm" onClick={() => handlePreset("front")}>
                  Front
                </button>
                <button className="btn-sm" onClick={() => handlePreset("iso")}>
                  Iso
                </button>
                <button className="btn-sm" onClick={() => handlePreset("reset")}>
                  Reset
                </button>
              </div>

              <UploadPanel onUploaded={onUploaded} />
            </div>

            <div className="studio-canvas-wrapper relative rounded-md overflow-hidden bg-gray-50">
              {dragging && (
                <div className="absolute inset-0 z-40 flex items-center justify-center bg-black/20 pointer-events-none">
                  <div className="rounded-md bg-white/80 p-6 shadow-lg">
                    Drop files here to load
                  </div>
                </div>
              )}

              <SceneCanvas ref={sceneRef} onDragState={setDragging} />
            </div>
          </div>

          {/* RIGHT PANEL */}
          <div className="col-span-3 space-y-4">
            <UIPanel title="Material">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div
                    className="w-10 h-6 rounded border"
                    style={{ background: material.color }}
                  />
                  <label className="text-sm">Base Color</label>
                </div>

                <div>
                  <label className="text-xs">Roughness</label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.01"
                    value={material.roughness}
                    onChange={(e) =>
                      setMaterial({ roughness: parseFloat(e.target.value) })
                    }
                  />
                </div>

                <div>
                  <label className="text-xs">Metalness</label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.01"
                    value={material.metalness}
                    onChange={(e) =>
                      setMaterial({ metalness: parseFloat(e.target.value) })
                    }
                  />
                </div>
              </div>
            </UIPanel>

            <UIPanel title="Textures">
              <div className="space-y-2">
                <input type="file" accept="image/*" />
                <input type="file" accept="image/*" />
              </div>
            </UIPanel>

            <UIPanel title="Environment">
              <HDRISelector />
            </UIPanel>

            <UIPanel title="Model Library">
              <ModelLibrary />
            </UIPanel>

            <UIPanel title="Presets">
              <PresetCategories />
              <PresetGallery />
            </UIPanel>

            <div className="flex gap-2">
              <button className="btn" onClick={undo}>Undo</button>
              <button className="btn" onClick={redo}>Redo</button>
              <button className="btn-outline">Export Pack</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
