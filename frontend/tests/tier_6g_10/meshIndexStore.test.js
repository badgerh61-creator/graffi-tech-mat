import { setMeshPathsForObject, meshIndexGetSnapshot, clearMeshIndex } from "../../src/editor/scene/meshIndexStore";

test("setMeshPathsForObject stores sorted unique list", () => {
  clearMeshIndex();
  setMeshPathsForObject("vehicle-1", ["b", "a", "a"]);
  const m = meshIndexGetSnapshot().meshPathsByObjectId["vehicle-1"];
  expect(m).toEqual(["a", "b"]);
});

test("clearMeshIndex wipes state", () => {
  clearMeshIndex();
  setMeshPathsForObject("x", ["a"]);
  clearMeshIndex();
  expect(meshIndexGetSnapshot().meshPathsByObjectId).toEqual({});
});
