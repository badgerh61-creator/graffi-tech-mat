import { validateSnap } from "../../src/editor/transform/validateSnap";

test("passes when disabled", () => {
  expect(validateSnap(false, 0).ok).toBe(true);
});

test("fails when enabled and step <= 0", () => {
  const r = validateSnap(true, 0);
  expect(r.ok).toBe(false);
  if (!r.ok) expect(r.reason).toBe("invalid_snap_step");
});

test("passes when enabled and finite step > 0", () => {
  expect(validateSnap(true, 0.25).ok).toBe(true);
});
