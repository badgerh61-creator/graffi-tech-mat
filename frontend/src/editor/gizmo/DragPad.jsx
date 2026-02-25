import React, { useEffect, useMemo, useRef, useState } from "react";

/**
 * DragPad (Tier 7.26)
 * - UI-only drag surface
 * - commits once on release
 * - supports both PointerEvents and MouseEvents (test-friendly)
 */
export default function DragPad({
  enabled,
  label,
  axisLabel,
  scale = 0.01,
  mode,
  onPreview,
  onCommit,
}) {
  const ref = useRef(null);
  const [dragging, setDragging] = useState(false);
  const [start, setStart] = useState(null);
  const [value, setValue] = useState(null);

  const help = useMemo(() => {
    if (mode === "translate") return `Δ = pixels * ${scale}`;
    if (mode === "rotate") return `deg = pixels * ${scale}`;
    return `factor = 1 + pixels * ${scale}`;
  }, [mode, scale]);

  useEffect(() => {
    function onKeyDown(e) {
      if (e.key === "Escape" && dragging) {
        setDragging(false);
        setStart(null);
        setValue(null);
        onPreview?.(null);
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [dragging, onPreview]);

  function begin(clientX, clientY) {
    if (!enabled) return;
    setDragging(true);
    setStart({ x: clientX, y: clientY });
    setValue(0);
    onPreview?.(0);
  }

  function move(clientX, clientY) {
    if (!enabled || !dragging || !start) return;

    const dx = clientX - start.x;
    const dy = clientY - start.y;

    // deterministic: use dominant axis (dx or -dy)
    const pixels = Math.abs(dx) >= Math.abs(dy) ? dx : -dy;

    let v;
    if (mode === "translate") v = pixels * scale;
    else if (mode === "rotate") v = pixels * scale;
    else v = 1 + pixels * scale;

    setValue(v);
    onPreview?.(v);
  }

  function end() {
    if (!enabled || !dragging) return;

    setDragging(false);
    setStart(null);

    const v = value;
    setValue(null);
    onPreview?.(null);

    if (v === null || v === undefined) return;
    onCommit?.(v);
  }

  // Pointer handlers (real app)
  function onPointerDown(e) {
    begin(e.clientX, e.clientY);
    try {
      e.currentTarget.setPointerCapture?.(e.pointerId);
    } catch {}
  }
  function onPointerMove(e) {
    move(e.clientX, e.clientY);
  }
  function onPointerUp() {
    end();
  }

  // Mouse handlers (tests / fallback)
  function onMouseDown(e) {
    begin(e.clientX, e.clientY);
  }
  function onMouseMove(e) {
    move(e.clientX, e.clientY);
  }
  function onMouseUp() {
    end();
  }
  function onMouseLeave() {
    // if user drags out then releases elsewhere, treat as end
    end();
  }

  return (
    <div className="border rounded p-2 space-y-1">
      <div className="flex items-center justify-between">
        <div className="text-xs font-semibold">
          {label}{" "}
          {axisLabel ? <span className="opacity-70">({axisLabel})</span> : null}
        </div>
        <div className="text-[11px] opacity-70">{help}</div>
      </div>

      <div
        ref={ref}
        className={`border rounded h-16 flex items-center justify-center select-none ${
          enabled ? "cursor-ew-resize" : "opacity-50"
        }`}
        role="button"
        aria-label={`dragpad-${label}`}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        onMouseDown={onMouseDown}
        onMouseMove={onMouseMove}
        onMouseUp={onMouseUp}
        onMouseLeave={onMouseLeave}
      >
        <div className="text-xs opacity-80">
          {enabled ? (dragging ? "Dragging…" : "Drag here") : "Disabled"}
        </div>
      </div>

      {dragging ? (
        <div className="text-xs opacity-80">
          Preview: {value === null ? "-" : String(value.toFixed?.(4) ?? value)}
        </div>
      ) : null}
    </div>
  );
}
