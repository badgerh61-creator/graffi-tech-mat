import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import DecalsPanel from "../../src/editor/decals/DecalsPanel";

describe("Tier 7.37 DecalsPanel", () => {
  it("emits DECAL_CREATE payload", () => {
    const onCommitTool = vi.fn();
    render(
      <DecalsPanel
        snapshot={{ decor_state: { decals: [] } }}
        activeTargetId={"obj-1::CarRoot"}
        onCommitTool={onCommitTool}
      />
    );

    fireEvent.click(screen.getByText("Create Decal"));
    const payload = onCommitTool.mock.calls[0][0];

    expect(payload.tool).toBe("DECAL_CREATE");
    expect(payload.station).toBe("decor");
    expect(payload.payload.target_id).toContain("obj-1");
  });
});
