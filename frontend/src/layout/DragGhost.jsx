// frontend/src/layout/DragGhost.jsx

import React, { useEffect, useState } from "react";
import { usePanelDrag } from "./usePanelDrag";
import { panelRegistry } from "../panels/_panelRegistry";

/**
 * DragGhost
 * Visual-only floating preview of the panel being dragged.
 */
export default function DragGhost() {
  const { draggingPanel, isDragging } = usePanelDrag();
  const [pos, setPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    if (!isDragging) {
      return;
    }

    function onMouseMove(e) {
      setPos({
        x: e.clientX + 12,
        y: e.clientY + 12,
      });
    }

    window.addEventListener("mousemove", onMouseMove);
    return () =>
      window.removeEventListener("mousemove", onMouseMove);
  }, [isDragging]);

  if (!isDragging || !draggingPanel) {
    return null;
  }

  const panelDef = panelRegistry[draggingPanel];

  if (!panelDef) {
    return null;
  }

  return (
    <div
      className="drag-ghost"
      style={{
        position: "fixed",
        top: pos.y,
        left: pos.x,
        pointerEvents: "none",
        zIndex: 9999,
      }}
    >
      <div className="drag-ghost__panel">
        {panelDef.title}
      </div>
    </div>
  );
}

