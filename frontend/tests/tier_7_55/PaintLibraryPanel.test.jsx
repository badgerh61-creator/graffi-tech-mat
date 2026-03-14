import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import PaintLibraryPanel from "../../src/editor/materials/PaintLibraryPanel";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "obj-1::Body/MainMesh::slot:BodyPaint" }),
}));

vi.mock("../../src/services/studio/paintLibraryApi", () => ({
  fetchPaintLibrary: async () => [
    { id: "paint_gloss_red", name: "Gloss Red", finish: "gloss" },
    { id: "paint_matte_black", name: "Matte Black", finish: "matte" },
  ],
}));

describe("PaintLibraryPanel", () => {
  it("renders paint library", async () => {
    render(
      <PaintLibraryPanel
        snapshot={{ decor_state: { paint_swatches: [] } }}
        canEdit={true}
        onCommitTool={vi.fn()}
      />
    );

    expect(screen.getByText("Paint Library")).toBeTruthy();
    expect(await screen.findByText("Apply Paint Preset")).toBeTruthy();
    expect(await screen.findByText("Save Swatch")).toBeTruthy();
  });
});
