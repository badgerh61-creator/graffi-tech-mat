import { buildMeshPath } from "../../src/editor/scene/meshPath";

function node(name) {
  return { name, parent: null, children: [] };
}

function link(parent, child) {
  child.parent = parent;
  parent.children.push(child);
  return child;
}

test("builds path from names", () => {
  const group = node("obj:vehicle-1");
  const a = link(group, node("CarRoot"));
  const b = link(a, node("Body"));
  const m = link(b, node("Door_L"));

  expect(buildMeshPath(m)).toBe("CarRoot/Body/Door_L");
});

test("uses unnamed index fallback deterministically", () => {
  const group = node("obj:vehicle-1");
  const a = link(group, node("CarRoot"));
  link(a, node("")); // unnamed-0 under CarRoot
  const c = link(a, node("")); // unnamed-1 under CarRoot
  const m = link(c, node("")); // unnamed-0 under unnamed-1

  expect(buildMeshPath(m)).toBe("CarRoot/unnamed-1/unnamed-0");
});

test("stops at obj: boundary", () => {
  const group = node("obj:vehicle-1");
  const m = link(group, node("WheelFL"));

  expect(buildMeshPath(m)).toBe("WheelFL");
});
