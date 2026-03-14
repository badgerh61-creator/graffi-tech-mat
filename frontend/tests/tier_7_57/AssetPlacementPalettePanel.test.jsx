import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import AssetPlacementPalettePanel from "../../src/editor/assets/AssetPlacementPalettePanel";

vi.mock("../../src/services/studio/modelAssetsApi", () => ({
  fetchModelAssets: async () => [
    {
      id: "asset-vehicle-demo",
      name: "Demo Vehicle",
      kind: "vehicle",
      category: "vehicles",
      tags: ["demo"],
    },
  ],
}));

describe("AssetPlacementPalettePanel", () => {
  it("renders asset palette", async () => {
    render(
      <AssetPlacementPalettePanel
        canEdit={true}
        onCommitTool={vi.fn()}
      />
    );

    expect(screen.getByText("Asset Placement Palette")).toBeTruthy();

    await screen.findByText("Demo Vehicle");
  });
});
