import {
  ensureKind,
  layersGetSnapshot,
  setKindVisible,
  setKindPickable,
  setKindOpacity,
} from "../../src/editor/scene/layersStore";

test("ensureKind creates deterministic defaults", () => {
  const a = ensureKind("vehicle");
  expect(a.visible).toBe(true);
  expect(a.pickable).toBe(true);
  expect(a.opacity).toBe(1.0);

  const h = ensureKind("helper");
  expect(h.pickable).toBe(false);
});

test("setKindVisible toggles visibility", () => {
  ensureKind("vehicle");
  setKindVisible("vehicle", false);
  expect(layersGetSnapshot().kinds.vehicle.visible).toBe(false);
});

test("opacity clamps to [0,1]", () => {
  ensureKind("vehicle");
  setKindOpacity("vehicle", 2);
  expect(layersGetSnapshot().kinds.vehicle.opacity).toBe(1);

  setKindOpacity("vehicle", -1);
  expect(layersGetSnapshot().kinds.vehicle.opacity).toBe(0);
});

test("pickable toggle works", () => {
  ensureKind("vehicle");
  setKindPickable("vehicle", false);
  expect(layersGetSnapshot().kinds.vehicle.pickable).toBe(false);
});
