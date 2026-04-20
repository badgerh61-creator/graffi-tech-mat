import {
  beginLoad,
  isLoadValid,
  clearLoad
} from "../../src/editor/scene/assetManager";

test("latest load wins", () => {
  const id = "obj";

  const a = beginLoad(id);
  const b = beginLoad(id);

  expect(isLoadValid(id, a)).toBe(false);
  expect(isLoadValid(id, b)).toBe(true);
});

test("clear removes load", () => {
  const id = "obj2";

  const r = beginLoad(id);
  clearLoad(id);

  expect(isLoadValid(id, r)).toBe(false);
});
