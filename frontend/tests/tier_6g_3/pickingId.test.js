import { buildPickedTargetId } from "../../src/editor/scene/pickingId";

test("uses mesh.name when present", () => {
  const id = buildPickedTargetId({ objectId: "vehicle-1", mesh: { name: "DoorMesh", uuid: "u1" } });
  expect(id).toBe("vehicle-1::DoorMesh");
});

test("falls back to uuid", () => {
  const id = buildPickedTargetId({ objectId: "vehicle-1", mesh: { name: "", uuid: "u2" } });
  expect(id).toBe("vehicle-1::u2");
});
