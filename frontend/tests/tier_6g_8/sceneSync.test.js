import {
  getObjectIdFromSelectedId,
  sceneIndexObjectIds,
  isSelectionValidForSceneIndex,
  makeSceneRebindKey,
} from "../../src/editor/scene/sceneSync";

test("getObjectIdFromSelectedId extracts object id", () => {
  expect(getObjectIdFromSelectedId("vehicle-1::CarRoot/Body/Door_L")).toBe("vehicle-1");
});

test("getObjectIdFromSelectedId returns null on invalid", () => {
  expect(getObjectIdFromSelectedId("no_delim")).toBe(null);
  expect(getObjectIdFromSelectedId("")).toBe(null);
});

test("sceneIndexObjectIds collects ids", () => {
  const ids = sceneIndexObjectIds({
    objects: [{ id: "vehicle-1" }, { id: 2 }, null, {}],
  });
  expect(ids).toEqual(["vehicle-1", "2"]);
});

test("isSelectionValidForSceneIndex true when nothing selected", () => {
  expect(isSelectionValidForSceneIndex(null, { objects: [{ id: "a" }] })).toBe(true);
});

test("isSelectionValidForSceneIndex checks object presence", () => {
  const scene = { objects: [{ id: "vehicle-1" }, { id: "wheel-1" }] };
  expect(isSelectionValidForSceneIndex("vehicle-1::X", scene)).toBe(true);
  expect(isSelectionValidForSceneIndex("missing::X", scene)).toBe(false);
});

test("makeSceneRebindKey deterministic", () => {
  expect(makeSceneRebindKey(null)).toBe("snap:none");
  expect(makeSceneRebindKey(10)).toBe("snap:10");
  expect(makeSceneRebindKey("10")).toBe("snap:10");
});
