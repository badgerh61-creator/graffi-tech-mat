import { parseSelectedId, findNodeByMeshPath } from "../../src/editor/scene/selectionResolve";

function node(name) {
  return { name, children: [] };
}
function link(parent, child) {
  parent.children.push(child);
  return child;
}

test("parseSelectedId handles object-only selection", () => {
  expect(parseSelectedId("vehicle-1::")).toEqual({ objectId: "vehicle-1", meshPath: null });
});

test("parseSelectedId handles mesh selection", () => {
  expect(parseSelectedId("vehicle-1::CarRoot/Body/Door_L")).toEqual({
    objectId: "vehicle-1",
    meshPath: "CarRoot/Body/Door_L",
  });
});

test("findNodeByMeshPath resolves name chain", () => {
  const root = node("obj:vehicle-1");
  const a = link(root, node("CarRoot"));
  const b = link(a, node("Body"));
  const c = link(b, node("Door_L"));

  const got = findNodeByMeshPath(root, "CarRoot/Body/Door_L");
  expect(got).toBe(c);
});

test("findNodeByMeshPath supports unnamed indices", () => {
  const root = node("obj:vehicle-1");
  const a = link(root, node("CarRoot"));
  const x0 = link(a, node(""));
  const x1 = link(a, node(""));
  const m = link(x1, node(""));

  const got = findNodeByMeshPath(root, "CarRoot/unnamed-1/unnamed-0");
  expect(got).toBe(m);
});

test("findNodeByMeshPath returns null when missing", () => {
  const root = node("obj:vehicle-1");
  link(root, node("CarRoot"));
  expect(findNodeByMeshPath(root, "CarRoot/Nope")).toBe(null);
});
