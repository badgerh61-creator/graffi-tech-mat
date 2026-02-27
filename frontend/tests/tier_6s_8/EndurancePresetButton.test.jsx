import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";
import EndurancePresetButton from "../../src/editor/telemetry/EndurancePresetButton";

describe("EndurancePresetButton", () => {
  it("emits endurance engine + scenario", () => {
    const onApply = vi.fn();
    render(<EndurancePresetButton onApply={onApply} />);

    fireEvent.click(screen.getByText("Use Endurance Settings"));
    expect(onApply).toHaveBeenCalled();

    const arg = onApply.mock.calls[0][0];
    expect(arg.engine_version).toBe("pseudo-endurance-v1");
    expect(arg.scenario).toBeTruthy();
    expect(arg.scenario.duration_s).toBeDefined();
  });
});
