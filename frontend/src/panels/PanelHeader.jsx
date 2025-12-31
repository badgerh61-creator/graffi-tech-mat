// frontend/src/panels/PanelHeader.jsx

import React from "react";
import { usePanelDrag } from "../layout/usePanelDrag";

/**
 * PanelHeader
 * Draggable header that emits drag intent only.
 */
export default function PanelHeader({ panelId, title }) {
  const { beginDrag, cancelDrag } = usePanelDrag();

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
      className="panel-header cursor-move select-none"
      draggable
      onDragStart={onDragStart}
      onDragEnd={onDragEnd}
    >
      {title}
    </header>
  );
}

