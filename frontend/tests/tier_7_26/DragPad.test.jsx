import React from "react"; // ✅ add this line
import { render, fireEvent, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import DragPad from "../../src/editor/gizmo/DragPad";

describe("DragPad", () => {
  it("commits once on mouse up", () => {
    const onCommit = vi.fn();

    render(
      <DragPad
        enabled={true}
        label="Translate"
        axisLabel="X"
        mode="translate"
        scale={0.02}
        onCommit={onCommit}
      />
    );

    const pad = screen.getByLabelText("dragpad-Translate");

    fireEvent.mouseDown(pad, { clientX: 100, clientY: 100 });
    fireEvent.mouseMove(pad, { clientX: 150, clientY: 100 });
    fireEvent.mouseUp(pad, { clientX: 150, clientY: 100 });

    expect(onCommit).toHaveBeenCalledTimes(1);
    expect(onCommit.mock.calls[0][0]).toBeCloseTo(1.0, 5);
  });

  it("does nothing when disabled", () => {
    const onCommit = vi.fn();

    render(
      <DragPad
        enabled={false}
        label="Rotate"
        axisLabel="Y"
        mode="rotate"
        scale={0.2}
        onCommit={onCommit}
      />
    );

    const pad = screen.getByLabelText("dragpad-Rotate");

    fireEvent.mouseDown(pad, { clientX: 100, clientY: 100 });
    fireEvent.mouseMove(pad, { clientX: 200, clientY: 100 });
    fireEvent.mouseUp(pad, { clientX: 200, clientY: 100 });

    expect(onCommit).toHaveBeenCalledTimes(0);
  });
});
