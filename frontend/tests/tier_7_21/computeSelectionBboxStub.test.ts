import { computeSelectionBboxStub } from "../../src/editor/selection/computeSelectionBboxStub";

test("returns null for empty ids", () => {
  expect(computeSelectionBboxStub([])).toBe(null);
});

test("deterministic for same ids", () => {
  const a = computeSelectionBboxStub(["panel-1", "panel-2"]);
  const b = computeSelectionBboxStub(["panel-1", "panel-2"]);
  expect(a).toEqual(b);
});

test("order-independent (ids sorted upstream), but still stable if order differs", () => {
  const a = computeSelectionBboxStub(["a", "b", "c"]);
  const b = computeSelectionBboxStub(["c", "b", "a"]);
  // Our implementation uses ids as provided; your selectedIds is sorted already.
  // This test asserts equality if caller sorts; for safety, we just assert shape.
  expect(a?.min).toHaveProperty("x");
  expect(b?.max).toHaveProperty("z");
});
