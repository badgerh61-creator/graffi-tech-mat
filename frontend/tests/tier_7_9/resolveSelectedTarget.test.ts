import { describe, it, expect } from "vitest";
import { resolveSelectedTarget } from "../../src/editor/selection/resolveSelectedTarget";

describe("tier_7_9 resolveSelectedTarget", () => {
  it("rejects when no snapshot", () => {
    const r = resolveSelectedTarget(null as any, "panel-1");
    expect(r.targetId).toBeNull();
  });

  it("rejects when nothing selected", () => {
    const r = resolveSelectedTarget({ id: 1 } as any, null);
    expect(r.targetId).toBeNull();
  });

  it("accepts selected id", () => {
    const r = resolveSelectedTarget({ id: 1 } as any, "panel-1");
    expect(r.targetId).toBe("panel-1");
  });
});
