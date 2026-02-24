import { validatePivot } from "../../src/editor/transform/validatePivot";

test("passes for non-custom modes", () => {
  expect(validatePivot("bbox_center", { x: NaN, y: NaN, z: NaN }).ok).toBe(true);
});

test("fails for custom when any value not finite", () => {
  const r = validatePivot("custom", { x: 1, y: NaN, z: 3 });
  expect(r.ok).toBe(false);
  if (!r.ok) expect(r.reason).toBe("invalid_pivot");
});

test("passes for custom when xyz are finite", () => {
  const r = validatePivot("custom", { x: 1, y: 2, z: 3 });
  expect(r.ok).toBe(true);
});
