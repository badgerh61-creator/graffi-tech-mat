import { describe, it, expect, vi, beforeEach } from "vitest";
import { evaluateProposal } from "../../src/services/studio/assistantProposalsApi";

beforeEach(() => {
  global.fetch = vi.fn() as any;
});

describe("assistantProposalsApi", () => {
  it("calls evaluate with correct body shape", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ allowed: true }),
    });

    const res = await evaluateProposal({
      snapshotId: 12,
      proposal: { station: "geometry", tool: "TRANSLATE", payload: { x: 1 } },
      getAccessToken: () => "t",
    });

    expect(res.allowed).toBe(true);

    const [url, opts] = (global.fetch as any).mock.calls[0];
    expect(String(url)).toContain("/assistant/proposals/evaluate");

    const body = JSON.parse(opts.body);
    expect(body.snapshot_id).toBe(12);
    expect(body.proposal.tool).toBe("TRANSLATE");
  });
});
