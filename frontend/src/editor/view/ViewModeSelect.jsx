import { useViewMode, setViewMode } from "./viewModeStore";

export default function ViewModeSelect() {
  const { mode } = useViewMode();

  return (
    <div className="border rounded px-2 py-1 flex items-center gap-2">
      <div className="text-xs opacity-70">View</div>
      <select
        className="border rounded px-2 py-1 text-sm"
        value={mode}
        onChange={(e) => setViewMode(e.target.value)}
      >
        <option value="studio">Studio</option>
        <option value="solid">Solid</option>
        <option value="clay">Clay</option>
        <option value="wireframe">Wireframe</option>
      </select>
    </div>
  );
}
