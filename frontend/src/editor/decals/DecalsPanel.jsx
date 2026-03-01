// frontend/src/editor/decals/DecalsPanel.jsx
import React, { useMemo, useState } from "react";

const BLENDS = ["normal", "multiply", "add"];

function clamp01(x) {
  const n = Number(x);
  if (!Number.isFinite(n)) return 1;
  return Math.max(0, Math.min(1, n));
}

export default function DecalsPanel({
  snapshot,
  activeTargetId,
  onCommitTool, // (payload) => governed evaluate/apply
}) {
  const decals = useMemo(() => snapshot?.decor_state?.decals || [], [snapshot]);
  const [assetRef, setAssetRef] = useState("builtin://checker");
  const [opacity, setOpacity] = useState(1.0);
  const [blend, setBlend] = useState("normal");
  const [selectedId, setSelectedId] = useState(decals?.[0]?.id || "");

  const selected = decals.find((d) => String(d.id) === String(selectedId));

  if (!snapshot) return null;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Decals</div>

      <div className="text-xs opacity-70">
        Target: {activeTargetId || "none"} · Count: {decals.length}
      </div>

      {/* CREATE */}
      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold opacity-80">Create</div>

        <label className="text-xs flex items-center justify-between gap-2">
          <span>asset_ref</span>
          <input
            className="border rounded px-2 py-1 flex-1"
            value={assetRef}
            onChange={(e) => setAssetRef(e.target.value)}
            placeholder="builtin://checker"
          />
        </label>

        <label className="text-xs flex items-center justify-between gap-2">
          <span>opacity</span>
          <input
            className="border rounded px-2 py-1 w-24"
            type="number"
            step="0.05"
            value={opacity}
            onChange={(e) => setOpacity(clamp01(e.target.value))}
          />
        </label>

        <label className="text-xs flex items-center justify-between gap-2">
          <span>blend</span>
          <select
            className="border rounded px-2 py-1"
            value={blend}
            onChange={(e) => setBlend(e.target.value)}
          >
            {BLENDS.map((b) => (
              <option key={b} value={b}>
                {b}
              </option>
            ))}
          </select>
        </label>

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!activeTargetId || !assetRef}
          onClick={() =>
            onCommitTool?.({
              tool: "DECAL_CREATE",
              station: "decor",
              payload: {
                target_id: activeTargetId,
                asset_ref: assetRef,
                initial: {
                  position: { x: 0, y: 0, z: 0 },
                  rotation_euler: { x: 0, y: 0, z: 0 },
                  scale: { x: 1, y: 1, z: 1 },
                  opacity: clamp01(opacity),
                  blend,
                  z_offset: 0.001,
                  meta: { name: "Decal" },
                },
              },
            })
          }
        >
          Create Decal
        </button>
      </div>

      {/* LIST + SELECT */}
      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold opacity-80">Existing</div>

        <select
          className="border rounded px-2 py-1 text-sm w-full"
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value)}
        >
          <option value="">(none)</option>
          {decals.map((d) => (
            <option key={d.id} value={d.id}>
              {d.meta?.name || d.id} — {String(d.asset_ref || "")}
            </option>
          ))}
        </select>

        {!selected ? (
          <div className="text-xs opacity-70">No decal selected.</div>
        ) : (
          <div className="space-y-2">
            <div className="text-xs opacity-70">id: {selected.id}</div>

            <button
              className="border rounded px-3 py-2 text-sm"
              onClick={() =>
                onCommitTool?.({
                  tool: "DECAL_UPDATE",
                  station: "decor",
                  payload: {
                    decal_id: selected.id,
                    patch: { enabled: !selected.enabled },
                  },
                })
              }
            >
              {selected.enabled ? "Disable" : "Enable"}
            </button>

            <button
              className="border rounded px-3 py-2 text-sm"
              onClick={() =>
                onCommitTool?.({
                  tool: "DECAL_DELETE",
                  station: "decor",
                  payload: { decal_id: selected.id },
                })
              }
            >
              Delete
            </button>
          </div>
        )}
      </div>

      <div className="text-[11px] opacity-60">
        Decals are governed edits stored in decor_state. No painting in this tier.
      </div>
    </div>
  );
}
