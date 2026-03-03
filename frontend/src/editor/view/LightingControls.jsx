import { useLighting, setLighting } from "./lightingStore";

export default function LightingControls() {
  const l = useLighting();

  return (
    <div className="border rounded p-2 flex items-center gap-3">
      <label className="text-sm flex items-center gap-2">
        <input
          type="checkbox"
          checked={!!l.enabled}
          onChange={(e) => setLighting({ enabled: e.target.checked })}
        />
        Studio Lighting
      </label>

      <label className="text-sm flex items-center gap-2">
        Exposure
        <input
          className="border rounded px-2 py-1 w-24"
          type="number"
          step="0.1"
          value={l.exposure}
          onChange={(e) => setLighting({ exposure: Number(e.target.value || 1) })}
        />
      </label>

      <label className="text-sm flex items-center gap-2">
        Env
        <input
          className="border rounded px-2 py-1 w-24"
          type="number"
          step="0.1"
          value={l.envIntensity}
          onChange={(e) => setLighting({ envIntensity: Number(e.target.value || 1) })}
        />
      </label>
    </div>
  );
}
