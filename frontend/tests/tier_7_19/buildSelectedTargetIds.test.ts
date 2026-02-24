import { buildSelectedTargetIds } from "../../src/editor/selection/buildSelectedTargetIds";

test("returns [] when no primary", () => {
  expect(buildSelectedTargetIds({ primary: null, secondary: [] })).toEqual([]);
});

test("returns sorted unique ids (primary + secondary)", () => {
  const selection = {
    primary: { kind: "panel", id: "b" },
    secondary: [{ kind: "panel", id: "a" }, { kind: "panel", id: "c" }, { kind: "panel", id: "a" }],
  };
  expect(buildSelectedTargetIds(selection)).toEqual(["a", "b", "c"]);
});
