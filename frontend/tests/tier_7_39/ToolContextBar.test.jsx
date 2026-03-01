import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import ToolContextBar from "../../src/editor/toolbar/ToolContextBar";

describe("ToolContextBar", () => {
  it("shows blocked reasons", () => {
    render(<ToolContextBar canEdit={false} reasons={["NOT_DRAFT", "NO_LOCK"]} />);
    expect(screen.getByText("NOT_DRAFT")).toBeTruthy();
    expect(screen.getByText("NO_LOCK")).toBeTruthy();
  });
});
