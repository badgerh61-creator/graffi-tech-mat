import { parseSelectedId } from "../../src/editor/scene/selectionResolve";

test("parses non-instance selectedId", () => {
  expect(parseSelectedId("vehicle-1::CarRoot/Body")).toEqual({
    objectKey: "vehicle-1",
    objectId: "vehicle-1",
    instanceId: null,
    meshPath: "CarRoot/Body",
  });
});

test("parses instance selectedId", () => {
  expect(parseSelectedId("wheel@inst-02::Rim/Mesh")).toEqual({
    objectKey: "wheel@inst-02",
    objectId: "wheel",
    instanceId: "inst-02",
    meshPath: "Rim/Mesh",
  });
});

test("parses instance object-only selection", () => {
  expect(parseSelectedId("wheel@inst-02::")).toEqual({
    objectKey: "wheel@inst-02",
    objectId: "wheel",
    instanceId: "inst-02",
    meshPath: null,
  });
});
