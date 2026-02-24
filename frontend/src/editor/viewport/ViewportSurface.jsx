// frontend/src/editor/viewport/ViewportSurface.jsx
import React from "react";
import {
  useSelection,
  clearSelection,
  applyResolvedSelectionToStore,
} from "../selection/selectionStore";
import { resolveSelectionRemote } from "../selection/resolveSelectionClient";

/**
 * Engine-independent picking surface.
 * Clickable "proxy objects" are DOM nodes with data-target-id.
 *
 * Tier 7.18:
 * - click behavior resolved deterministically via backend /selection/resolve (Tier 7.6)
 * - supports Shift (toggle) and Ctrl (add)
 * - store remains unified (legacy selectedId + typed primary/secondary bridged)
 */
export default function ViewportSurface({ disabled = false }) {
  const { selectedId, primary, secondary } = useSelection();
  const typedId = primary?.id ?? null;

  async function onClick(e) {
    if (disabled) return;

    const el = e.target.closest("[data-target-id]");
    const tid = el?.getAttribute("data-target-id");

    const hitCandidates = tid
      ? [{ target_id: tid, kind: "panel", depth: 0.1, priority: 0 }]
      : [];

    const modifiers = {
      shift: !!e.shiftKey,
      ctrl: !!e.ctrlKey,
    };

    const previousSelection = {
      selected_target_ids: [
        ...(primary?.id ? [primary.id] : []),
        ...(secondary?.map((s) => s.id) ?? []),
      ].sort(),
      active_target_id: primary?.id ?? null,
    };

    try {
      const resolved = await resolveSelectionRemote({
        hitCandidates,
        modifiers,
        previousSelection,
      });

      applyResolvedSelectionToStore(resolved);
    } catch (err) {
      console.warn("selection resolve failed:", err);

      // deterministic fallback: empty click clears if no modifiers
      if (!tid && !modifiers.shift && !modifiers.ctrl) {
        clearSelection();
      }
    }
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
          <span className="ml-2 opacity-70">(Shift=toggle, Ctrl=add)</span>
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
