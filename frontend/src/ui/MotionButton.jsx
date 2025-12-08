// src/ui/MotionButton.jsx
import React from "react";
import { motion } from "framer-motion";

export default function MotionButton({ children, className = "", ...props }) {
  return (
    <motion.button
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.18 }}
      className={`btn ${className}`}
      {...props}
    >
      {children}
    </motion.button>
  );
}
