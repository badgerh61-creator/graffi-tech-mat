// src/ui/ModelLibrary.jsx
import React from "react";
import { motion } from "framer-motion";
import { useAssetStore } from "../store/assetStore";
import { useModelStore } from "../store/modelStore";

export default function ModelLibrary() {
  const assets = useAssetStore((s) => s.assets ?? []);
  const removeAsset = useAssetStore((s) => s.removeAsset ?? (() => {}));
  const setCurrentModel = useModelStore((s) => s.setCurrentModel ?? (() => {}));

  const hasAssets = Array.isArray(assets) && assets.length > 0;

  return (
    <div className="p-3">
      <div className="flex items-center justify-between mb-2">
        <div className="text-sm font-medium">Model Library</div>
      </div>

      {!hasAssets && (
        <div className="text-sm text-slate-500">No models uploaded</div>
      )}

      {hasAssets && (
        <div className="grid grid-cols-1 gap-2">
          {assets.map((a) => (
            <motion.div
              key={a.id}
              className="flex items-center gap-2 p-2 bg-ui-surface rounded-lg border border-ui-border"
              whileHover={{ scale: 1.01 }}
            >
              <div className="h-12 w-12 bg-slate-200 rounded flex items-center justify-center text-xs">
                {(a.name ?? "MD").slice(0, 2).toUpperCase()}
              </div>

              <div className="flex-1 text-sm">
                <div className="font-medium truncate">{a.name ?? "Unknown"}</div>
                <div className="text-xs text-slate-500">
                  {Math.round((a.size ?? 0) / 1024)} KB
                </div>
              </div>

              <div className="flex flex-col items-end gap-1">
                <button
                  onClick={() => setCurrentModel(a.id)}
                  className="text-xs px-2 py-1 bg-ui-button text-ui-text rounded"
                >
                  Open
                </button>

                <button
                  onClick={() => removeAsset(a.id)}
                  className="text-xs text-rose-600"
                >
                  Delete
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
