// frontend/src/layout/DockDropZone.jsx

import React, { useState } from "react";
import { usePanelDrag } from "./usePanelDrag";

/**
 * DockDropZone
 * UI-only drop target that signals panel drag intent.
 */
export default function DockDropZone({
  dock,
  index = undefined,
  className = "",
  children,
}) {
  const { dropPanel } = usePanelDrag();
  const [hovering, setHovering] = useState(false);

  function onDragOver(e) {
    e.preventDefault();
    setHovering(true);
  }

  function onDragLeave() {
    setHovering(false);
  }

  function onDrop(e) {
    e.preventDefault();
    setHovering(false);
    dropPanel(dock, index);
  }

  return (
    <div
      data-dock={dock}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
      className={`
        dock-drop-zone
        transition-colors
        ${hovering ? "outline outline-2 outline-indigo-500" : ""}
        ${className}
      `}
    >
      {children}
    </div>
  );
}

