import { applyDecals } from "../../src/editor/scene/applyDecals";

test("applyDecals safe", async () => {
  await applyDecals(null, []);
  expect(true).toBe(true);
});
