import { useEffect, useMemo, useState } from "react";
import { getAccessToken } from "../../utils/auth";
import { listTemplates, createScenarioFromTemplate } from "../../services/simulationTemplatesApi";

export default function ScenarioTemplatesPanel({ projectId, onCreated }) {
  const token = useMemo(() => getAccessToken?.(), []);
  const [templates, setTemplates] = useState([]);
  const [selected, setSelected] = useState("");
  const [name, setName] = useState("New Scenario");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  useEffect(() => {
    setErr(null);
    listTemplates({ token })
      .then((d) => setTemplates(d.templates || []))
      .catch((e) => setErr(String(e?.message || e)));
  }, [token]);

  async function onCreate() {
    if (!projectId || !selected || !name) return;
    setBusy(true); setErr(null);
    try {
      const out = await createScenarioFromTemplate({
        projectId,
        name,
        templateKey: selected,
        engineVersion: "pseudo-v1",
        overrides: {},
        token,
      });
      onCreated?.(out);
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Scenario Templates (6S.6)</div>
      {err ? <div className="text-xs border rounded p-2">Error: {err}</div> : null}

      <label className="text-xs">
        Scenario name
        <input className="border rounded w-full px-2 py-1" value={name} onChange={(e) => setName(e.target.value)} />
      </label>

      <label className="text-xs">
        Template
        <select className="border rounded w-full px-2 py-1" value={selected} onChange={(e) => setSelected(e.target.value)}>
          <option value="">Select…</option>
          {templates.map((t) => (
            <option key={t.key} value={t.key}>
              {t.name} ({t.key})
            </option>
          ))}
        </select>
      </label>

      <button className="border rounded px-3 py-1 text-sm" disabled={busy || !projectId || !selected || !name} onClick={onCreate}>
        {busy ? "Creating..." : "Create Scenario"}
      </button>
    </div>
  );
}
