// src/ui/ModelLibrary.jsx
import React, { useEffect } from "react";
import { useModelStore } from "../store/modelStore";

export default function ModelLibrary() {
  const models = useModelStore((s) => s.models);
  const fetchModels = useModelStore((s) => s.fetchModels);
  const openModel = useModelStore((s) => s.openModel);
  const currentModelId = useModelStore((s) => s.currentModelId);
  const modelStatus = useModelStore((s) => s.modelStatus);

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
      {models.map((m) => {
        const isActive = currentModelId === m.id;
        const isLoading = modelStatus === "loading";

        return (
          <button
            key={m.id}
            onClick={() => !isLoading && openModel(m.id)}
            disabled={isLoading}
            className={`
              w-full text-left px-3 py-2 rounded border
              transition
              ${isActive
                ? "bg-slate-200 border-slate-400"
                : "bg-white border-ui-border"}
              ${isLoading
                ? "opacity-60 cursor-wait"
                : "hover:bg-ui-button cursor-pointer"}
            `}
          >
            <div className="flex items-center justify-between">
              <span className="truncate">{m.name}</span>

              {m.role && (
                <span className="ml-2 text-xs bg-amber-100 text-amber-700 px-1 rounded">
                  {m.role}
                </span>
              )}
            </div>
          </button>
        );
      })}
    </div>
  );
}

