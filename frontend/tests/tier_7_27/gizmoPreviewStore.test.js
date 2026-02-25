import { clearGizmoPreview, previewGetSnapshot, setGizmoPreview } from "../../src/editor/gizmo/gizmoPreviewStore";

test("preview store sets and clears", () => {
  clearGizmoPreview();
  expect(previewGetSnapshot().preview).toBe(null);

  setGizmoPreview({ target_id: "a", tool: "TRANSLATE", payload: { target_id: "a" } });
  expect(previewGetSnapshot().preview.tool).toBe("TRANSLATE");

  clearGizmoPreview();
  expect(previewGetSnapshot().preview).toBe(null);
});
