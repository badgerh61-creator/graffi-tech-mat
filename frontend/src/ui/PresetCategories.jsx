// src/ui/PresetCategories.jsx
import React from "react";
import { motion } from "framer-motion";
import { useMaterialCategoryStore } from "../store/materialCategoryStore";

const CATEGORIES = [
  "all",
  "metal",
  "plastic",
  "wood",
  "glass",
  "fabric",
  "custom",
];

export default function PresetCategories() {
  const selectedCategory = useMaterialCategoryStore(
    (s) => s.selectedCategory
  );
  const setCategory = useMaterialCategoryStore(
    (s) => s.setCategory
  );

  return (
    <div className="p-3 border-b border-ui-border">
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map((cat) => {
          const active = selectedCategory === cat;

          return (
            <motion.button
              key={cat}
              whileTap={{ scale: 0.96 }}
              onClick={() => setCategory(cat)}
              className={`text-xs px-3 py-1 rounded-full border transition ${
                active
                  ? "bg-ui-accent text-white border-ui-accent"
                  : "bg-ui-surface text-ui-text border-ui-border hover:bg-ui-button"
              }`}
            >
              {cat.toUpperCase()}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}

