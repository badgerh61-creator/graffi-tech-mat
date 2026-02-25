import { buildRotatePayload, buildScalePayload } from "../../src/editor/gizmo/payloadBuilders";

test("buildRotatePayload snaps degrees deterministically", () => {
  const p = buildRotatePayload({
    targetId: "vehicle-1::CarRoot/Door_L",
    axis: "y",
    rawDegrees: 13,
    snap: { enabled: true, step_degrees: 5 },
  });

  expect(p.tool).toBe("ROTATE");
  expect(p.station).toBe("geometry");
  expect(p.payload.target_id).toContain("vehicle-1::");
  expect(p.payload.axis).toBe("y");
  expect(p.payload.degrees).toBe(15);
  expect(p.payload.snap.step_degrees).toBe(5);
});

test("buildScalePayload snaps factor deterministically", () => {
  const p = buildScalePayload({
    targetId: "vehicle-1::CarRoot/Door_L",
    axis: "uniform",
    rawFactor: 1.12,
    snap: { enabled: true, step_factor: 0.05 },
  });

  expect(p.tool).toBe("SCALE");
  expect(p.station).toBe("geometry");
  expect(p.payload.axis).toBe("uniform");
  // nearest 0.05 to 1.12 => 1.10
  expect(p.payload.factor).toBe(1.1);
  expect(p.payload.snap.step_factor).toBe(0.05);
});
