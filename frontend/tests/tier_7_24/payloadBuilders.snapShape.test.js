import { buildTranslatePayload } from "../../src/editor/gizmo/payloadBuilders";

test("translate payload includes snap shape", () => {
  const p = buildTranslatePayload({
    targetId: "panel-1",
    axis: "x",
    rawDelta: { x: 0.1, y: 0, z: 0 },
    snap: { enabled: true, step: 0.25 },
  });

  expect(p.payload.snap.enabled).toBe(true);
  expect(p.payload.snap.step).toBe(0.25);
});
