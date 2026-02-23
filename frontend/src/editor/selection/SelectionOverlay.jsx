import { setSelectedId, clearSelection, useSelection } from "./selectionStore";

/**
 * Temporary selection UI.
 * Replace later with viewport picking.
 */
export default function SelectionOverlay() {
  const { selectedId } = useSelection();

  const items = [
    { id: "panel-1", label: "Panel 1" },
    { id: "panel-2", label: "Panel 2" },
    { id: "door-left", label: "Door Left" },
  ];

  return (
    <div className="p-2 border rounded space-y-2">
      <div className="text-sm font-semibold">Selection</div>

      <div className="space-y-1">
        {items.map((it) => (
          <button
            key={it.id}
            onClick={() => setSelectedId(it.id)}
            className={`w-full text-left px-2 py-1 rounded border ${
              selectedId === it.id ? "opacity-100" : "opacity-80"
            }`}
          >
            {it.label} <span className="opacity-60">({it.id})</span>
          </button>
        ))}
      </div>

      <button onClick={clearSelection} className="px-2 py-1 rounded border w-full">
        Clear
      </button>

      <div className="text-xs opacity-75">
        Active: {selectedId ? selectedId : "none"}
      </div>
    </div>
  );
}
