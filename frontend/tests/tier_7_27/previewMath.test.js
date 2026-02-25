import { makeRotatePreview, makeScalePreview, makeTranslatePreview } from "../../src/editor/gizmo/previewMath";

test("translate preview snaps deterministically", () => {
  const p = makeTranslatePreview({
    targetId: "vehicle-1::CarRoot",
    axis: "x",
    rawDeltaAxis: 0.13,
    snap: { enabled: true, step: 0.25 },
  });
  expect(p.tool).toBe("TRANSLATE");
  expect(p.payload.delta.x).toBe(0.25);
});

test("rotate preview snaps degrees deterministically", () => {
  const p = makeRotatePreview({
    targetId: "vehicle-1::CarRoot",
    axis: "y",
    rawDegrees: 13,
    snap: { enabled: true, step_degrees: 5 },
  });
  expect(p.tool).toBe("ROTATE");
  expect(p.payload.degrees).toBe(15);
});

test("scale preview snaps + clamps deterministically", () => {
  const p = makeScalePreview({
    targetId: "vehicle-1::CarRoot",
    axis: "uniform",
    rawFactor: 1.12,
    snap: { enabled: true, step_factor: 0.05 },
  });
  expect(p.tool).toBe("SCALE");
  expect(p.payload.factor).toBe(1.1);
});
