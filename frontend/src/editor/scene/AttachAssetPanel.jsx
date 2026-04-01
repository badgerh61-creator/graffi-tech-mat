import { useEffect, useState, useMemo } from "react";
import { listAssets, attachAsset } from "../../services/studio/assetsApi";

export default function AttachAssetPanel({ projectId, snapshotId, onAttached }) {
  const [assets, setAssets] = useState([]);
  const [assetId, setAssetId] = useState("");
  const [objectId, setObjectId] = useState("vehicle-1");
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    listAssets()
      .then((r) => setAssets(r.items || []))
      .catch((e) => setErr(String(e?.message || e)));
  }, []);

  const disabledReason = useMemo(() => {
    if (!projectId) return "missing projectId";
    if (!snapshotId) return "missing snapshotId (active snapshot not ready yet)";
    if (!assetId) return "select an asset first";
    if (busy) return "busy";
    return null;
  }, [projectId, snapshotId, assetId, busy]);
   
  console.log("🧪 ATTACH CLICK", {
    projectId,
    snapshotId,
    assetId,
    busy,
  });
 
  async function onAttach() {
    if (!projectId || !snapshotId || !assetId) return;

    setErr(null);
    setBusy(true);

    const payload = {
      object_id: objectId,
      asset_id: Number(assetId),
      kind: "vehicle",
    };

    // 🔎 debug publish
    window.__dbg_lastAttachPayload = payload;

    try {
      const resp = await attachAsset(projectId, snapshotId, payload);

      // 🔎 debug publish
      window.__dbg_attachAsset_response = resp;

      onAttached?.();
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Attach Asset (6G.2)</div>

      {/* 🔎 always-visible debug */}
      <div className="text-xs opacity-70">
        projectId: <b>{String(projectId)}</b> · snapshotId:{" "}
        <b>{snapshotId ? String(snapshotId) : "none"}</b> · assetId:{" "}
        <b>{assetId ? String(assetId) : "none"}</b>
        {disabledReason ? (
          <>
            {" "}
            · <span className="text-red-600">disabled: {disabledReason}</span>
          </>
        ) : null}
      </div>

      {err ? <div className="text-sm text-red-600">{err}</div> : null}

      <div>
        <div className="text-xs opacity-70">Object ID</div>
        <input
          className="border rounded px-2 py-1 w-full"
          value={objectId}
          onChange={(e) => setObjectId(e.target.value)}
        />
      </div>

      <div>
        <div className="text-xs opacity-70">Asset</div>
        <select
          className="border rounded px-2 py-1 w-full"
          value={assetId}
          onChange={(e) => setAssetId(e.target.value)}
        >
          <option value="">Select asset…</option>
          {assets.map((a) => (
            <option key={a.id} value={a.id}>
              #{a.id} — {a.filename} ({a.processed ? "ready" : "not-ready"})
            </option>
          ))}
        </select>
      </div>

      <button
        className="border rounded px-3 py-1 text-sm"
        disabled={!!disabledReason}
        title={disabledReason || ""}
        onClick={onAttach}
      >
        {busy ? "Attaching…" : "Attach"}
      </button>

      <div className="text-xs opacity-70">
        Writes asset_ref as <code>asset:&lt;id&gt;</code> into snapshot.body_state.scene.objects[] (draft only).
      </div>
    </div>
  );
}
