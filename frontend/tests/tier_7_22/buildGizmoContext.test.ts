import { buildGizmoContext } from "../../src/editor/gizmo/buildGizmoContext";

test("returns null when no primary", () => {
  const ctx = buildGizmoContext({
    selection: { primary: null, secondary: [], hovered: null, lastUpdatedAt: 0 },
    pivotMode: "bbox_center",
    customPivot: { x: 0, y: 0, z: 0 },
  });
  expect(ctx).toBe(null);
});

test("includes selected_target_ids and selection_bbox when multi", () => {
  const ctx = buildGizmoContext({
    selection: {
      primary: { kind: "panel", id: "b" },
      secondary: [{ kind: "panel", id: "a" }],
      hovered: null,
      lastUpdatedAt: 0,
    },
    pivotMode: "bbox_center",
    customPivot: { x: 0, y: 0, z: 0 },
  });

  expect(ctx?.target_id).toBe("b");
  expect(ctx?.selected_target_ids).toEqual(["a", "b"]);
  expect(ctx?.selection_bbox).toBeTruthy();
});
