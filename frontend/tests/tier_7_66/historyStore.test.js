import { describe, it, expect } from "vitest";
import {
  historyPush,
  historyUndo,
  historyRedo,
  historyGetSnapshot,
} from "../../src/editor/history/historyStore";

describe("historyStore", () => {
  it("moves cursor correctly", () => {
    historyPush("a");
    historyPush("b");
    historyPush("c");

    expect(historyGetSnapshot().cursor).toBe(2);

    historyUndo();
    expect(historyGetSnapshot().cursor).toBe(1);

    historyUndo();
    expect(historyGetSnapshot().cursor).toBe(0);

    historyRedo();
    expect(historyGetSnapshot().cursor).toBe(1);
  });
});
