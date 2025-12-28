// src/ui/ModelLibrary.jsx
import React, { useEffect } from "react";
import { useModelStore } from "../store/modelStore";

export default function ModelLibrary() {
  const models = useModelStore((s) => s.models);
  const fetchModels = useModelStore((s) => s.fetchModels);
  const openModel = useModelStore((s) => s.openModel);

  useEffect(() => {
    fetchModels();
  }, [fetchModels]);

  if (!models.length) {
    return (
      <div className="text-sm text-slate-500">
        No models uploaded yet
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {models.map((m) => (
        <button
          key={m.id}
          onClick={() => openModel(m.id)}   // ✅ SINGLE SOURCE OF TRUTH
          className="w-full text-left px-3 py-2 rounded bg-ui-surface border border-ui-border hover:bg-ui-button"
        >
          {m.name}
          {m.role && (
            <span className="ml-2 text-xs bg-amber-100 text-amber-700 px-1 rounded">
              {m.role}
            </span>
          )}
        </button>
      ))}
    </div>
  );
}

