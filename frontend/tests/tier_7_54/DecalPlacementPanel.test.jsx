import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import DecalPlacementPanel from "../../src/editor/decals/DecalPlacementPanel";

describe("DecalPlacementPanel", () => {
  it("renders placement controls", () => {
    render(<DecalPlacementPanel />);

    expect(
      screen.getByRole("heading", { name: /decal placement/i })
    ).toBeTruthy();

    expect(
      screen.getByRole("checkbox", { name: /placement mode/i })
    ).toBeTruthy();

    expect(
      screen.getByRole("button", { name: /reset placement tool/i })
    ).toBeTruthy();
  });
});
