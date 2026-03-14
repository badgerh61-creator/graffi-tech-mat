import { describe, it, expect } from "vitest";
import {
  detectSelectionKind,
  computeInspectorSections,
} from "../../src/editor/inspector/inspectorContext";

describe("inspectorContext", () => {
  it("detects slot selection", () => {
    expect(
      detectSelectionKind({
        selectedId: "obj-1::Body/MainMesh::slot:BodyPaint",
        activeDecalId: null,
      })
    ).toBe("slot");
  });

  it("prefers decal kind when active decal exists", () => {
    expect(
      detectSelectionKind({
        selectedId: "obj-1",
        activeDecalId: "dec-1",
      })
    ).toBe("decal");
  });

  it("returns deterministic sections", () => {
    const r = computeInspectorSections({
      selectedId: "obj-1::MeshA",
      activeDecalId: null,
      placementEnabled: false,
      violations: [{ constraint_id: "c1" }],
    });

    expect(r.sections).toContain("summary");
    expect(r.sections).toContain("materials");
    expect(r.sections).toContain("paint");
    expect(r.sections).toContain("constraints");
  });
});
