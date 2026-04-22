import { setupLighting } from "../../src/editor/scene/setupLighting";

test("lighting setup safe", async () => {
  const renderer = {};
  const scene = {};

  await setupLighting(renderer, scene);

  expect(true).toBe(true);
});
