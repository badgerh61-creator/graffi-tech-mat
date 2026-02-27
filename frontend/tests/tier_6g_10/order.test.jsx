import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import SceneGraphPanel from "../../src/editor/scene/SceneGraphPanel";

// mock selection store
vi.mock("../../src/editor/selection/selectionStore", () => {
  let selectedId = null;
  return {
    useSelection: () => ({ selectedId }),
    setSelectedId: (v) => { selectedId = v; },
    clearSelection: () => { selectedId = null; },
  };
});

// mock mesh index
vi.mock("../../src/editor/scene/meshIndexStore", () => {
  return {
    useMeshIndex: () => ({
      meshPathsByObjectId: {
        "vehicle-1": ["CarRoot/Body", "CarRoot/WheelFL"],
      },
    }),
  };
});

import { describe, it, expect, vi } from "vitest";

describe("SceneGraphPanel", () => {
  it("renders objects in deterministic order (kind then id)", () => {
    const sceneIndex = {
      objects: [
        { id: "b", kind: "vehicle", name: "B" },
        { id: "a", kind: "helper", name: "A" },
        { id: "a2", kind: "vehicle", name: "A2" },
      ],
    };

    render(<SceneGraphPanel sceneIndex={sceneIndex} />);

    // First object should be helper:a (kind helper sorts before vehicle)
    expect(screen.getByText("helper: A")).toBeTruthy();
    expect(screen.getByText("vehicle: A2")).toBeTruthy();
    expect(screen.getByText("vehicle: B")).toBeTruthy();
  });

  it("expands and shows mesh paths when available", () => {
    const sceneIndex = { objects: [{ id: "vehicle-1", kind: "vehicle", name: "Car" }] };
    render(<SceneGraphPanel sceneIndex={sceneIndex} />);

    fireEvent.click(screen.getByText("▸"));
    expect(screen.getByText("CarRoot/Body")).toBeTruthy();
    expect(screen.getByText("CarRoot/WheelFL")).toBeTruthy();
  });
});
