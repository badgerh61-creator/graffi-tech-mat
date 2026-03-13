import { describe, it, expect } from "vitest";
import { buildOutlinerTree } from "../../src/editor/outliner/outlinerTree";

describe("buildOutlinerTree", () => {
  it("builds parent child hierarchy", () => {
    const tree = buildOutlinerTree([
      { id: "obj-2", parent_id: "obj-1", name: "Child" },
      { id: "obj-1", parent_id: null, name: "Parent" },
    ]);

    expect(tree.length).toBe(1);
    expect(tree[0].id).toBe("obj-1");
    expect(tree[0].children.length).toBe(1);
    expect(tree[0].children[0].id).toBe("obj-2");
  });
});
