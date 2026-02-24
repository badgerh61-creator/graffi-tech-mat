import { useSelection } from "./selectionStore";

export default function SelectionHud() {
  const sel = useSelection();
  const primary = sel.primary ? `${sel.primary.kind}:${sel.primary.id}` : "none";
  const secondaryCount = sel.secondary?.length ?? 0;

  return (
    <div className="border rounded px-3 py-2 text-xs opacity-90">
      <div>
        <span className="font-semibold">Primary:</span> {primary}
      </div>
      <div>
        <span className="font-semibold">Secondary:</span> {secondaryCount}
      </div>
    </div>
  );
}
