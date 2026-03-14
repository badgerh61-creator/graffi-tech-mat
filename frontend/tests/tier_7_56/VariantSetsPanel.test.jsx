import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import VariantSetsPanel from "../../src/editor/variants/VariantSetsPanel";

describe("VariantSetsPanel", () => {
  it("renders save/apply variant controls", () => {
    render(
      <VariantSetsPanel
        snapshot={{ decor_state: { variant_sets: [] } }}
        canEdit={true}
        onCommitTool={vi.fn()}
      />
    );

    expect(screen.getByText("Variant Sets")).toBeTruthy();
    expect(screen.getByText("Save Variant")).toBeTruthy();
    expect(screen.getByText("Apply Variant")).toBeTruthy();
  });
});
