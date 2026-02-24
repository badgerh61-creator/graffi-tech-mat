import React from "react";
import { useSelection, setPrimarySelection, clearSelection } from "../selection/selectionStore";

/**
 * Engine-independent picking surface.
 * Clickable "proxy objects" are DOM nodes with data-target-id.
 *
 * Tier 7.16 (unified store version):
 * - uses setPrimarySelection (typed) as canonical
 * - legacy selectedId stays bridged automatically inside selectionStore.js
 */
export default function ViewportSurface({ disabled = false }) {
  const { selectedId, primary } = useSelection();
  const typedId = primary?.id ?? null;

  function onClick(e) {
    if (disabled) return;

    const el = e.target.closest("[data-target-id]");
    const tid = el?.getAttribute("data-target-id");

    if (!tid) {
      clearSelection(); // your clearSelection already clears typed+legacy
      return;
    }

    // typed-first (canonical); selectionStore bridges selectedId automatically
    setPrimarySelection({ kind: "panel", id: tid });
  }

  const proxies = [
    { id: "panel-1", label: "Panel 1" },
    { id: "panel-2", label: "Panel 2" },
    { id: "door-left", label: "Door Left" },
  ];

  const shownSelected = typedId ?? selectedId ?? null;

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">Viewport (Stub)</div>
        <div className="text-xs opacity-75">Selected: {shownSelected ?? "none"}</div>
      </div>

      <div
        className={`border rounded p-3 min-h-[240px] ${disabled ? "opacity-60" : ""}`}
        onClick={onClick}
        role="button"
        aria-label="viewport-surface"
      >
        <div className="text-xs opacity-70 mb-2">
          Click any proxy object to select it. Click empty space to clear.
        </div>

        <div className="grid grid-cols-3 gap-2">
          {proxies.map((p) => (
            <div
              key={p.id}
              data-target-id={p.id}
              className={`border rounded p-2 text-sm cursor-pointer ${
                (typedId ?? selectedId) === p.id ? "opacity-100" : "opacity-85"
              }`}
            >
              {p.label}
              <div className="text-xs opacity-60">{p.id}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
