import { getAccessToken } from "../../utils/auth";
import { newProposalId } from "./proposalId";
import {
  evaluateProposal,
  previewProposal,
  applyProposal,
} from "./assistantProposalsApi";

const API_BASE = "http://127.0.0.1:8000";

/**
 * Normalized ExecResult:
 * { ok: true, data }
 * { ok: false, error: { kind, status, detail } }
 */
function normalizeHttpError(status, detail) {
  const kind =
    status === 401
      ? "unauthenticated"
      : status === 403
      ? "forbidden"
      : status === 409
      ? "conflict"
      : status === 422
      ? "invalid"
      : status >= 500
      ? "server"
      : "server";

  return { ok: false, error: { kind, status, detail: detail || "" } };
}

async function safeJson(res) {
  try {
    return await res.json();
  } catch {
    return {};
  }
}

/**
 * Mode:
 * - "tools" (POST /tools/execute)
 * - "proposals" (evaluate -> apply; optional preview)
 *
 * Defaults to "proposals" because it's your safest AAA "official apply" path.
 */
export async function executeTool({
  snapshotId,
  station,
  tool,
  payload,
  mode = "proposals",
  enablePreview = false,
}) {
  try {
    if (mode === "tools") {
      const token = getAccessToken();
      const res = await fetch(`${API_BASE}/tools/execute`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          snapshot_id: snapshotId,
          station,
          tool,
          payload,
        }),
      });

      const data = await safeJson(res);
      if (!res.ok) return normalizeHttpError(res.status, data?.detail);

      return { ok: true, data };
    }

    // mode === "proposals"
    const proposal = { station, tool, payload };

    // 1) Evaluate
    const decision = await evaluateProposal({
      snapshotId,
      proposal,
      getAccessToken,
    });

    // Normalize "blocked" as conflict (because backend uses 409 for governance mismatch often)
    if (decision?.allowed === false) {
      return {
        ok: false,
        error: {
          kind: "conflict",
          status: 409,
          detail: decision.reason || "Tool rejected",
        },
        data: { decision },
      };
    }

    // 2) Preview (optional, non-blocking)
    let payloadHash = undefined;
    if (enablePreview) {
      try {
        const preview = await previewProposal({
          snapshotId,
          proposal,
          getAccessToken,
        });
        payloadHash = preview.payload_hash || preview.payloadHash;
      } catch {
        // non-blocking by contract
      }
    }

    // 3) Apply
    const applied = await applyProposal({
      proposalId: newProposalId(),
      snapshotId,
      payloadHash,
      getAccessToken,
    });

    return { ok: true, data: applied };
  } catch (e) {
    // Fetch/network or unexpected runtime error
    return {
      ok: false,
      error: { kind: "network", detail: String(e?.message || e) },
    };
  }
}
