import {
  setSceneIndex,
  getSceneSnapshot,
  subscribeScene
} from "../../src/editor/scene/sceneStore";

test("scene store updates deterministically", () => {
  setSceneIndex({ objects: [{ id: 1 }] }, 99);

  const state = getSceneSnapshot();

  expect(state.snapshotId).toBe(99);
  expect(state.sceneIndex.objects.length).toBe(1);
});

test("subscribers are notified on update", () => {
  let called = false;

  const unsub = subscribeScene(() => {
    called = true;
  });

  setSceneIndex({ objects: [] }, 1);

  unsub();

  expect(called).toBe(true);
});
