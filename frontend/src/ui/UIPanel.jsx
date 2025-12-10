// src/ui/UIPanel.jsx
import React from "react";
import { motion } from "framer-motion";

export default function UIPanel({ title, children, className = "" }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className={`bg-ui-surface border border-ui-border rounded-xl p-4 shadow card-shadow mb-4 ${className}`}
    >
      {title && <div className="text-sm font-semibold mb-3 text-ui-text/80">{title}</div>}
      {children}
    </motion.div>
  );
}
