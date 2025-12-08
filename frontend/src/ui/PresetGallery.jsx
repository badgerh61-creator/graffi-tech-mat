// src/ui/PresetGallery.jsx
import React from "react";
import { useMaterialPresetsStore } from "../store/materialPresetsStore";
import { useMaterialCategoryStore } from "../store/materialCategoryStore";
import { motion, AnimatePresence } from "framer-motion";

export default function PresetGallery({ onApply }) {
  const { presets, deletePreset } = useMaterialPresetsStore();
  const { selectedCategory } = useMaterialCategoryStore();

  const filtered =
    selectedCategory && selectedCategory !== "all"
      ? presets.filter((p) => p.category === selectedCategory)
      : presets;

  return (
    <div className="p-3">
      {filtered.length === 0 && (
        <div className="text-sm text-slate-400">
          No presets in this category
        </div>
      )}

      <div className="grid grid-cols-2 gap-3">
        <AnimatePresence>
          {filtered.map((p) => (
            <motion.div
              key={p.id}
              layout
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white/90 border rounded-lg p-2 flex flex-col"
            >
              <div className="h-28 bg-slate-100 rounded-md overflow-hidden flex items-center justify-center">
                {p.thumbnail ? (
                  <img
                    src={p.thumbnail}
                    alt={p.name}
                    className="object-cover w-full h-full"
                  />
                ) : (
                  <div className="text-sm text-slate-500">No preview</div>
                )}
              </div>

              <div className="mt-2 flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium">{p.name}</div>
                  <div className="text-xs text-slate-500">{p.category}</div>
                </div>

                <div className="flex flex-col gap-1">
                  <button
                    onClick={() => onApply?.(p)}
                    className="px-2 py-1 text-xs bg-indigo-600 text-white rounded"
                  >
                    Apply
                  </button>
                  <button
                    onClick={() => deletePreset(p.id)}
                    className="px-2 py-1 text-xs text-rose-600"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
