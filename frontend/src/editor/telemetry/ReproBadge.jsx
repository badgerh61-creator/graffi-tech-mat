import { useEffect, useMemo, useState } from "react";
import { getAccessToken } from "../../utils/auth";
import { getRunRepro } from "../../services/simulationReproApi";

export default function ReproBadge({ runId }) {
  const token = useMemo(() => getAccessToken?.(), []);
  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!runId) return;
    setErr(null);
    getRunRepro({ runId, token })
      .then(setData)
      .catch((e) => setErr(String(e?.message || e)));
  }, [runId, token]);

  if (!runId) return null;
  if (err) return <div className="text-xs border rounded p-2">Repro error: {err}</div>;
  if (!data) return <div className="text-xs opacity-70">Loading repro…</div>;

  const ok = !!data.verified_deterministic;

  async function copy() {
    try {
      await navigator.clipboard.writeText(data.run_fingerprint || "");
    } catch {}
  }

  return (
    <div className="border rounded p-2 text-xs space-y-1">
      <div className="flex items-center justify-between">
        <div className="font-semibold">Repro</div>
        <div className={`px-2 py-0.5 rounded border ${ok ? "" : "opacity-70"}`}>
          {ok ? "Verified Deterministic" : "Unverified"}
        </div>
      </div>

      <div className="opacity-80">fingerprint: {data.run_fingerprint}</div>
      <button className="border rounded px-2 py-1" onClick={copy}>Copy</button>
    </div>
  );
}
