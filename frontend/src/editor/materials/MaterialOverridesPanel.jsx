import { useMemo } from "react";

export default function MaterialOverridesPanel({ snapshot }) {
  const overrides = useMemo(
    () => snapshot?.body_state?.material_overrides || [],
    [snapshot]
  );

  if (!snapshot) return null;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Material Overrides</div>

      {!overrides.length ? (
        <div className="text-xs opacity-70">No overrides in this snapshot.</div>
      ) : (
        <div className="space-y-2">
          {overrides.map((o) => (
            <div key={o.id} className="border rounded p-2">
              <div className="text-xs font-semibold">
                {o.enabled === false ? "⛔ " : ""}{o.id}
              </div>
              <div className="text-[11px] opacity-75">
                target: {o?.target?.object_key}::{o?.target?.mesh_path || "(all meshes)"}
              </div>
              <pre className="text-[11px] opacity-80 overflow-auto mt-1">
{JSON.stringify(o.material || {}, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      )}

      <div className="text-xs opacity-70">
        Draft-only visual metadata. No mutation from this panel (yet).
      </div>
    </div>
  );
}
