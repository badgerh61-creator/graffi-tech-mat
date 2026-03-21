import React, { act } from "react";
import { describe, it, expect, vi } from "vitest";
import { render } from "@testing-library/react";
import { useKeyboardShortcuts } from "../../src/editor/input/useKeyboardShortcuts";

function Test({ onAction }) {
  useKeyboardShortcuts({ onAction });
  return null;
}

function fire(key, opts = {}) {
  act(() => {
    window.dispatchEvent(
      new KeyboardEvent("keydown", {
        key,
        bubbles: true,
        ...opts,
      })
    );
  });
}

describe("keyboardShortcuts", () => {
  it("G → translate", () => {
    const fn = vi.fn();
    render(<Test onAction={fn} />);
    fire("g");
    expect(fn).toHaveBeenCalledWith("TRANSFORM_TRANSLATE");
  });

  it("R → rotate", () => {
    const fn = vi.fn();
    render(<Test onAction={fn} />);
    fire("r");
    expect(fn).toHaveBeenCalledWith("TRANSFORM_ROTATE");
  });

  it("S → scale", () => {
    const fn = vi.fn();
    render(<Test onAction={fn} />);
    fire("s");
    expect(fn).toHaveBeenCalledWith("TRANSFORM_SCALE");
  });

  it("Ctrl+Z → undo", () => {
    const fn = vi.fn();
    render(<Test onAction={fn} />);
    fire("z", { ctrlKey: true });
    expect(fn).toHaveBeenCalledWith("UNDO");
  });

  it("Ctrl+Y → redo", () => {
    const fn = vi.fn();
    render(<Test onAction={fn} />);
    fire("y", { ctrlKey: true });
    expect(fn).toHaveBeenCalledWith("REDO");
  });

  it("Ctrl+Shift+Z → redo", () => {
    const fn = vi.fn();
    render(<Test onAction={fn} />);
    fire("z", { ctrlKey: true, shiftKey: true });
    expect(fn).toHaveBeenCalledWith("REDO");
  });

  it("Ctrl+D → duplicate", () => {
    const fn = vi.fn();
    render(<Test onAction={fn} />);
    fire("d", { ctrlKey: true });
    expect(fn).toHaveBeenCalledWith("DUPLICATE");
  });

  it("Escape → clear selection", () => {
    const fn = vi.fn();
    render(<Test onAction={fn} />);
    fire("Escape");
    expect(fn).toHaveBeenCalledWith("CLEAR_SELECTION");
  });
});
