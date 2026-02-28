import { composeTransform } from "../../src/editor/scene/composeTransform";

test("composeTransform adds positions and rotations, multiplies scales", () => {
  const out = composeTransform(
    {
      position: { x: 1, y: 2, z: 3 },
      rotation: { x: 0.1, y: 0.2, z: 0.3 },
      scale: { x: 2, y: 2, z: 2 },
    },
    {
      position: { x: 10, y: 0, z: -1 },
      rotation: { x: 0, y: 0.1, z: 0 },
      scale: { x: 0.5, y: 1, z: 2 },
    }
  );

  expect(out.position).toEqual({ x: 11, y: 2, z: 2 });
  expect(out.rotation.y).toBeCloseTo(0.3);
  expect(out.scale).toEqual({ x: 1, y: 2, z: 4 });
});

test("composeTransform safe defaults", () => {
  const out = composeTransform(null, null);
  expect(out.position).toEqual({ x: 0, y: 0, z: 0 });
  expect(out.scale).toEqual({ x: 1, y: 1, z: 1 });
});
