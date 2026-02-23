/**
 * Stub only:
 * - No Three.js handle logic here yet
 * - Emits deterministic deltas via callbacks
 */
export default function TransformGizmoStub({ onDragDelta }) {
  return (
    <div style={{ padding: 12, border: "1px dashed #aaa", borderRadius: 8 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Gizmo (stub)</div>
      <button onClick={() => onDragDelta({ x: 1, y: 0, z: 0 })}>Drag +X</button>{" "}
      <button onClick={() => onDragDelta({ x: 0, y: 1, z: 0 })}>Drag +Y</button>{" "}
      <button onClick={() => onDragDelta({ x: 0, y: 0, z: 1 })}>Drag +Z</button>
    </div>
  );
}
