import { useEffect, useMemo } from "react";
import {
  ensureKind,
  setKindPickable,
  setKindVisible,
  setKindOpacity,
  useSceneLayers,
} from "./layersStore";

export default function SceneLayersPanel({ sceneIndex }) {
  const layers = useSceneLayers();

  const kindsInScene = useMemo(() => {
    const objs = sceneIndex?.objects || [];
    const ks = new Set();
    for (const o of objs) {
      if (o?.kind) ks.add(String(o.kind));
      else ks.add("unknown");
    }
    return Array.from(ks).sort();
  }, [sceneIndex]);

  useEffect(() => {
    kindsInScene.forEach((k) => ensureKind(k));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [kindsInScene.join("|")]);

  if (!sceneIndex) {
    return (
      <div className="border rounded p-3 text-sm opacity-75">
        Scene Layers (loading scene…)
      </div>
    );
  }

  if (!kindsInScene.length) {
    return (
      <div className="border rounded p-3 text-sm opacity-75">
        Scene Layers (no objects)
      </div>
    );
  }

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="text-sm font-semibold">Scene Layers</div>

      <div className="space-y-2">
        {kindsInScene.map((k) => {
          const cfg = layers.kinds[k] || ensureKind(k);

          return (
            <div key={k} className="border rounded p-2 space-y-2">
              <div className="flex items-center justify-between">
                <div className="text-sm font-semibold">{k}</div>
                <div className="text-xs opacity-70">
                  vis:{cfg.visible ? "on" : "off"} / pick:{cfg.pickable ? "on" : "off"}
                </div>
              </div>

              <div className="flex items-center gap-3 text-sm">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={cfg.visible}
                    onChange={(e) => setKindVisible(k, e.target.checked)}
                  />
                  Visible
                </label>

                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={cfg.pickable}
                    onChange={(e) => setKindPickable(k, e.target.checked)}
                  />
                  Pickable
                </label>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-xs opacity-70 w-14">Opacity</div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={cfg.opacity}
                  onChange={(e) => setKindOpacity(k, e.target.value)}
                  className="w-full"
                />
                <div className="text-xs opacity-70 w-10">{cfg.opacity.toFixed(2)}</div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="text-xs opacity-70">
        Layers are UI-only. They don’t change snapshots.
      </div>
    </div>
  );
}
