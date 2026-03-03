import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import ModelAssetPickerPanel from "../../src/editor/assets/ModelAssetPickerPanel";

vi.mock("../../src/services/studio/modelAssetsApi", () => ({
  fetchModelAssets: async () => [
    { id: "asset-vehicle-demo", name: "Demo Vehicle", tags: ["vehicle"] },
  ],
}));

describe("ModelAssetPickerPanel", () => {
  it("renders models", async () => {
    render(<ModelAssetPickerPanel canEdit={true} onCommitTool={() => {}} />);

    // Wait for async state update (useEffect → fetchModelAssets → setState)
    expect(await screen.findByText("Demo Vehicle")).toBeInTheDocument();

    // Optional: also verify header
    expect(screen.getByText("Model Assets")).toBeInTheDocument();
  });
});
