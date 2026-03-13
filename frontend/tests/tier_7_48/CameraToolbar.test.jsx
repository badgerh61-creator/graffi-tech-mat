import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import CameraToolbar from "../../src/editor/camera/CameraToolbar";

describe("CameraToolbar", () => {
  it("renders and triggers callbacks", () => {
    const onFrameScene = vi.fn();

    render(
      <CameraToolbar
        onFrameSelected={() => {}}
        onFrameScene={onFrameScene}
        onPreset={() => {}}
      />
    );

    fireEvent.click(screen.getByText("Frame Scene"));
    expect(onFrameScene).toHaveBeenCalledTimes(1);
  });
});
