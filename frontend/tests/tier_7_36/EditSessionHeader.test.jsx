import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import EditSessionHeader from "../../src/editor/modes/EditSessionHeader";

describe("Tier 7.36 EditSessionHeader", () => {
  it("shows NOT_DRAFT in reasons when completed", () => {
    render(
      <EditSessionHeader
        activeSnapshot={{ id: 1, status: "completed" }}
        lockStatus={{ state: "unknown" }}
        loading={false}
      />
    );
    expect(screen.getByText("NOT_DRAFT")).toBeTruthy();
  });

  it("requires NO_LOCK for draft when not owned", () => {
    render(
      <EditSessionHeader
        activeSnapshot={{ id: 2, status: "draft" }}
        lockStatus={{ state: "taken" }}
        loading={false}
      />
    );
    expect(screen.getByText("NO_LOCK")).toBeTruthy();
  });
});
