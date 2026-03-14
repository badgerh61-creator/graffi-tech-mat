import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import InspectorSummarySection from "../../src/editor/inspector/InspectorSummarySection";

describe("InspectorSummarySection", () => {
  it("renders summary fields", () => {
    render(
      <InspectorSummarySection
        selectedId="obj-1::MeshA"
        activeDecalId={null}
        selectionKind="mesh"
        activeSnapshot={{ id: 7, status: "draft" }}
        toolsEnabled={true}
        lockState="owned"
      />
    );

    expect(screen.getByText("Summary")).toBeTruthy();
    expect(screen.getByText(/Kind:/)).toBeTruthy();
    expect(screen.getByText(/Snapshot:/)).toBeTruthy();
  });
});
