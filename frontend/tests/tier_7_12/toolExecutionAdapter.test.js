import { describe, it, expect, vi, beforeEach } from "vitest";
import { executeTool } from "../../src/services/studio/toolExecutionAdapter";

vi.mock("../../src/utils/auth", () => ({
  getAccessToken: () => "TOKEN",
}));

// Mock the proposal API module used by adapter
vi.mock("../../src/services/studio/assistantProposalsApi", () => ({
  evaluateProposal: vi.fn(async () => ({ allowed: true })),
  previewProposal: vi.fn(async () => ({ payload_hash: "h" })),
  applyProposal: vi.fn(async () => ({ new_snapshot_id: 123 })),
}));

vi.mock("../../src/services/studio/proposalId", () => ({
  newProposalId: () => "pid-1",
}));

describe("tier_7_12 executeTool adapter", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("uses proposals flow by default (evaluate->apply)", async () => {
    const res = await executeTool({
      snapshotId: 10,
      station: "geometry",
      tool: "TRANSLATE",
      payload: { target_id: "panel-1", x: 1 },
    });

    expect(res.ok).toBe(true);
    if (res.ok) {
      expect(res.data.new_snapshot_id).toBe(123);
    }
  });

  it("can use /tools/execute when mode=tools", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ new_snapshot_id: 99 }),
    });

    const res = await executeTool({
      snapshotId: 10,
      station: "geometry",
      tool: "TRANSLATE",
      payload: { target_id: "panel-1", x: 1 },
      mode: "tools",
    });

    expect(res.ok).toBe(true);
    if (res.ok) expect(res.data.new_snapshot_id).toBe(99);

    const [url] = global.fetch.mock.calls[0];
    expect(url).toContain("/tools/execute");
  });

  it("normalizes /tools/execute 422 to invalid", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({ detail: "Invalid tool" }),
    });

    const res = await executeTool({
      snapshotId: 10,
      station: "geometry",
      tool: "NOPE",
      payload: {},
      mode: "tools",
    });

    expect(res.ok).toBe(false);
    if (!res.ok) {
      expect(res.error.kind).toBe("invalid");
      expect(res.error.status).toBe(422);
    }
  });
});
