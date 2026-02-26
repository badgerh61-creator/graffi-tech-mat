// frontend/tests/tier_7_28/historyStore.test.js
import { historyGetSnapshot, historyPush } from "../../src/editor/history/historyStore.js";

test("historyPush appends and moves cursor", () => {
  const s = historyGetSnapshot();
  s.stack = [];
  s.cursor = -1;

  historyPush(1);
  historyPush(2);

  expect(s.stack).toEqual(["1", "2"]);
  expect(s.cursor).toBe(1);
});

test("historyPush truncates forward history", () => {
  const s = historyGetSnapshot();
  s.stack = ["1", "2", "3"];
  s.cursor = 1;

  historyPush(99);

  expect(s.stack).toEqual(["1", "2", "99"]);
  expect(s.cursor).toBe(2);
});
