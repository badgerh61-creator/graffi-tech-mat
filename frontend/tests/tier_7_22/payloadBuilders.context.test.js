import { buildTranslatePayload } from "../../src/editor/gizmo/payloadBuilders";

test("mergeContext overwrites target_id and adds multiselect fields", () => {
  const p = buildTranslatePayload({
    targetId: "SHOULD_BE_OVERWRITTEN",
    axis: "x",
    rawDelta: { x: 0.1, y: 0, z: 0 },
    snap: { enabled: false, step: 0 },
    context: {
      target_id: "panel-1",
      selected_target_ids: ["a", "panel-1"],
      pivot_mode: "bbox_center",
      selection_bbox: { min: { x: 0, y: 0, z: 0 }, max: { x: 1, y: 1, z: 1 } },
    },
  });

  expect(p.payload.target_id).toBe("panel-1");
  expect(p.payload.selected_target_ids).toEqual(["a", "panel-1"]);
  expect(p.payload.pivot_mode).toBe("bbox_center");
  expect(p.payload.selection_bbox.max.x).toBe(1);
});
