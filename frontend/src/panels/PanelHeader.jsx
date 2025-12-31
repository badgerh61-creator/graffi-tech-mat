// frontend/src/panels/PanelHeader.jsx

import React from "react";
import { usePanelDrag } from "../layout/usePanelDrag";

/**
 * PanelHeader
 * Draggable header that emits drag intent only.
 */
export default function PanelHeader({ panelId, title }) {
  const { beginDrag, cancelDrag, isDragging } = usePanelDrag();

  function onDragStart(e) {
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/plain", panelId);
    beginDrag(panelId);
  }

  function onDragEnd() {
    cancelDrag();
  }

  return (
    <header
      draggable
      onDragStart={onDragStart}
      onDragEnd={onDragEnd}
      className={[
        "panel-header",
        "flex items-center",
        "px-2 py-1",
        "select-none",
        "text-sm font-medium",
        "cursor-grab active:cursor-grabbing",
        "transition-colors duration-100",
        "hover:bg-ui-hover",
        isDragging ? "opacity-80" : "",
      ].join(" ")}
    >
      {title}
    </header>
  );
}

