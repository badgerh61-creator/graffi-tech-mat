// src/ui/ModelLibrary.jsx
import React from "react";
import { motion } from "framer-motion";
import { useModelStore } from "../store/modelStore";

export default function ModelLibrary() {
  const models = useModelStore((s) => s.models);
  const removeModel = useModelStore((s) => s.removeModel);
  const setCurrentModel = useModelStore((s) => s.setCurrentModel);

  if (!models.length) {
    return <div className="p-3 text-sm text-slate-500">No models uploaded</div>;
  }

  return (
    <div className="p-3">
      {models.map((m) => (
        <motion.div
          key={m.id}
          className="flex items-center gap-2 p-2 bg-ui-surface rounded-lg border border-ui-border"
          whileHover={{ scale: 1.01 }}
        >
          <div className="h-12 w-12 bg-slate-200 rounded flex items-center justify-center text-xs">
            {(m.name ?? "MD").slice(0, 2).toUpperCase()}
          </div>

          <div className="flex-1 text-sm">
            <div className="font-medium truncate">{m.name}</div>
          </div>

          <div className="flex flex-col items-end gap-1">
            <button
              onClick={() => setCurrentModel(m.id)}
              className="text-xs px-2 py-1 bg-ui-button text-ui-text rounded"
            >
              Open
            </button>
            <button
              onClick={() => removeModel(m.id)}
              className="text-xs text-rose-600"
            >
              Delete
            </button>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
