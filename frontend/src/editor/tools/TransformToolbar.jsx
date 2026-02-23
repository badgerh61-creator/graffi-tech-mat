import { useToolExecute } from "./useToolExecute";

export default function TransformToolbar({
  activeSnapshot,
  isEditable,
  selectedId,
  station = "geometry",
  onNewSnapshot,
}) {
  const { execute } = useToolExecute();

  async function run(tool) {
    if (!isEditable) return;
    if (!activeSnapshot?.id) return;
    if (!selectedId) return;

    const payload = {
      target_id: selectedId,
      params:
        tool === "TRANSLATE"
          ? { x: 10, y: 0, z: 0 }
          : tool === "ROTATE"
          ? { axis: "y", degrees: 5 }
          : { factor: 1.05 },
    };

    const result = await execute({
      snapshotId: activeSnapshot.id,
      station,
      tool,
      payload,
    });

    onNewSnapshot?.(result.new_snapshot_id);
  }

  return (
    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
      <button disabled={!isEditable || !selectedId} onClick={() => run("TRANSLATE")}>
        Move
      </button>
      <button disabled={!isEditable || !selectedId} onClick={() => run("ROTATE")}>
        Rotate
      </button>
      <button disabled={!isEditable || !selectedId} onClick={() => run("SCALE")}>
        Scale
      </button>
      {!selectedId && <span style={{ opacity: 0.7 }}>Select a target to enable tools</span>}
    </div>
  );
}
