import { normalizeSceneObjects } from "../../src/editor/scene/sceneSerializer";

test("fills missing transform values deterministically", () => {
  const input = [
    {
      id: 1,
      transform: {
        position: { x: 5 },
      },
    },
  ];

  const out = normalizeSceneObjects(input);

  expect(out[0].transform.position.x).toBe(5);
  expect(out[0].transform.position.y).toBe(0);
  expect(out[0].transform.scale.x).toBe(1);
});

test("always returns consistent structure", () => {
  const out = normalizeSceneObjects([{}]);

  const obj = out[0];

  expect(obj.id).toBeDefined();
  expect(obj.transform.position.x).toBeDefined();
  expect(obj.transform.rotation.z).toBeDefined();
});
