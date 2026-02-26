import React from "react";
import { useMemo } from "react";
import { useSnapshotHistoryGraph } from "./useSnapshotHistoryGraph";
import { useHistory } from "./historyStore";

/**
 * Props:
 * - activeSnapshotId: number|string|null
 * - onNavigate(snapshotId): switch active snapshot in editor
 */
export default function SnapshotHistoryGraphPanel({ activeSnapshotId, onNavigate }) {
  const { data, err, loading } = useSnapshotHistoryGraph(activeSnapshotId);
  const h = useHistory();

  const backendNodes = useMemo(() => {
    if (!data?.nodes || !Array.isArray(data.nodes)) return null;

    // Expect nodes represent chain from current -> root (per Tier 7.28 service),
    // We show root -> current for readability.
    const chain = [...data.nodes].reverse();

    return {
      mode: "graph",
      hasParentLinks: !!data.has_parent_links,
      chain,
    };
  }, [data]);

  const fallback = useMemo(() => {
    const stack = h.stack || [];
    const cursor = h.cursor ?? -1;
    return { mode: "linear", stack, cursor };
  }, [h.stack, h.cursor]);

  const view = backendNodes || fallback;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">Snapshot History</div>
        <div className="text-xs opacity-70">
          {backendNodes ? "Graph" : "Linear (fallback)"}
        </div>
      </div>

      {loading ? <div className="text-xs opacity-80">Loading…</div> : null}
      {err && !backendNodes ? (
        <div className="text-xs border rounded p-2">
          <div className="font-semibold">History endpoint unavailable</div>
          <div className="opacity-80">{String(err.message || err)}</div>
          <div className="opacity-70 mt-1">Showing fallback local history.</div>
        </div>
      ) : null}

      {view.mode === "graph" ? (
        <GraphView chain={view.chain} activeSnapshotId={activeSnapshotId} onNavigate={onNavigate} />
      ) : (
        <LinearView stack={view.stack} cursor={view.cursor} onNavigate={onNavigate} />
      )}
    </div>
  );
}

function NodeButton({ id, active, onClick }) {
  return (
    <button
      className={`border rounded px-2 py-1 text-xs ${active ? "opacity-100" : "opacity-80"}`}
      onClick={onClick}
      title={`snapshot ${id}`}
    >
      {id}
    </button>
  );
}

function GraphView({ chain, activeSnapshotId, onNavigate }) {
  return (
    <div className="space-y-2">
      <div className="text-xs opacity-75">Root → Current</div>

      <div className="space-y-2">
        {chain.map((n) => {
          const isActive = String(n.id) === String(activeSnapshotId);
          const children = Array.isArray(n.children_ids) ? n.children_ids : [];
          return (
            <div key={n.id} className="border rounded p-2">
              <div className="flex items-center gap-2">
                <div className="text-xs opacity-70">Node</div>
                <NodeButton id={n.id} active={isActive} onClick={() => onNavigate?.(n.id)} />
                {n.parent_snapshot_id ? (
                  <div className="text-[11px] opacity-60">parent: {n.parent_snapshot_id}</div>
                ) : (
                  <div className="text-[11px] opacity-60">root</div>
                )}
              </div>

              {children.length ? (
                <div className="mt-2">
                  <div className="text-[11px] opacity-70">Children (branches)</div>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {children.map((cid) => (
                      <NodeButton
                        key={cid}
                        id={cid}
                        active={String(cid) === String(activeSnapshotId)}
                        onClick={() => onNavigate?.(cid)}
                      />
                    ))}
                  </div>
                </div>
              ) : (
                <div className="mt-2 text-[11px] opacity-60">No children</div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function LinearView({ stack, cursor, onNavigate }) {
  if (!stack?.length) return <div className="text-xs opacity-75">No history yet.</div>;

  return (
    <div className="space-y-2">
      <div className="text-xs opacity-75">Local stack</div>
      <div className="flex flex-wrap gap-2">
        {stack.map((id, i) => (
          <NodeButton
            key={`${id}-${i}`}
            id={id}
            active={i === cursor}
            onClick={() => onNavigate?.(id)}
          />
        ))}
      </div>
    </div>
  );
}
