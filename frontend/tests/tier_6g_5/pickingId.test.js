import { buildPickedTargetId } from "../../src/editor/scene/pickingId";

function node(name) {
  return { name, parent: null, children: [] };
}
function link(parent, child) {
  child.parent = parent;
  parent.children.push(child);
  return child;
}

test("buildPickedTargetId uses mesh_path", () => {
  const group = node("obj:vehicle-1");
  const a = link(group, node("CarRoot"));
  const m = link(a, node("Door_L"));

  const id = buildPickedTargetId({ objectId: "vehicle-1", mesh: m });
  expect(id).toBe("vehicle-1::CarRoot/Door_L");
});
