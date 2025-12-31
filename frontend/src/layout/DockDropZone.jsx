// frontend/src/layout/DockDropZone.jsx

import React from "react";
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

  function onDragOver(e) {
    e.preventDefault();
  }

  function onDrop(e) {
    e.preventDefault();
    dropPanel(dock, index);
  }

  return (
    <div
      className={`dock-drop-zone ${className}`}
      onDragOver={onDragOver}
      onDrop={onDrop}
      data-dock={dock}
    >
      {children}
    </div>
  );
}

