import React, { useEffect, useMemo, useState } from "react";
import { useSelection } from "../selection/selectionStore";
import { fetchPaintLibrary } from "../../services/studio/paintLibraryApi";

const FINISHES = ["all", "gloss", "matte", "satin", "metallic", "chrome_like"];

export default function PaintLibraryPanel({
  snapshot,
  canEdit,
  onCommitTool,
}) {
  const { selectedId } = useSelection();
  const [presets, setPresets] = useState([]);
  const [finish, setFinish] = useState("all");
  const [q, setQ] = useState("");
  const [selectedPreset, setSelectedPreset] = useState("");
  const [err, setErr] = useState(null);

  useEffect(() => {
    let alive = true;
    fetchPaintLibrary()
      .then((p) => {
        if (!alive) return;
        setPresets(p);
        setSelectedPreset(p?.[0]?.id || "");
      })
      .catch((e) => alive && setErr(e?.message || String(e)));
    return () => {
      alive = false;
    };
  }, []);

  const filtered = useMemo(() => {
    const s = q.trim().toLowerCase();
    return presets.filter((p) => {
      if (finish !== "all" && p.finish !== finish) return false;
      if (!s) return true;
      return (
        String(p.id).toLowerCase().includes(s) ||
        String(p.name || "").toLowerCase().includes(s) ||
        String(p.finish || "").toLowerCase().includes(s)
      );
    });
  }, [presets, finish, q]);

  useEffect(() => {
    if (!filtered.some((p) => p.id === selectedPreset)) {
      setSelectedPreset(filtered?.[0]?.id || "");
    }
  }, [filtered, selectedPreset]);

  const swatches = snapshot?.decor_state?.paint_swatches || [];
  const [swatchName, setSwatchName] = useState("New Swatch");
  const [swatchColor, setSwatchColor] = useState("#777777");
  const [swatchFinish, setSwatchFinish] = useState("gloss");
  const [selectedSwatchId, setSelectedSwatchId] = useState(
    swatches?.[0]?.id || ""
  );

  useEffect(() => {
    setSelectedSwatchId(swatches?.[0]?.id || "");
  }, [swatches.length]);

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="text-sm font-semibold">Paint Library</div>

      <div className="text-xs opacity-70">
        Target: <span className="font-mono">{selectedId || "none"}</span>
      </div>

      {!selectedId && (
        <div className="text-xs text-red-500">
          Select an object first
        </div>
      )}

      {err ? <div className="text-xs">Error: {err}</div> : null}

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold opacity-80">
          Library Presets
        </div>

        <div className="flex items-center gap-2">
          <select
            className="border rounded px-2 py-1 text-sm"
            value={finish}
            onChange={(e) => setFinish(e.target.value)}
          >
            {FINISHES.map((f) => (
              <option key={f} value={f}>
                {f}
              </option>
            ))}
          </select>

          <input
            className="border rounded px-2 py-1 text-sm flex-1"
            placeholder="Search paints..."
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>

        <select
          className="border rounded px-2 py-1 text-sm w-full"
          value={selectedPreset}
          onChange={(e) => setSelectedPreset(e.target.value)}
        >
          {filtered.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} — {p.finish}
            </option>
          ))}
        </select>

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !selectedId || !selectedPreset}
          onClick={() => {
            if (!selectedId) {
              console.warn("❌ No target selected");
              return;
            }

            console.log("🔥 APPLY PRESET", {
              target_id: selectedId,
              preset_id: selectedPreset,
            });

            onCommitTool?.({
              tool: "PAINT_APPLY_LIBRARY_PRESET",
              station: "materials",
              payload: {
                target_id: selectedId,
                preset_id: selectedPreset,
              },
            });
          }}
        >
          Apply Paint Preset
        </button>
      </div>

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold opacity-80">
          Saved Swatches
        </div>

        <div className="grid grid-cols-3 gap-2">
          <input
            className="border rounded px-2 py-1 text-sm"
            value={swatchName}
            onChange={(e) => setSwatchName(e.target.value)}
            placeholder="Swatch name"
          />
          <input
            className="border rounded px-2 py-1 text-sm font-mono"
            value={swatchColor}
            onChange={(e) => setSwatchColor(e.target.value)}
            placeholder="#RRGGBB"
          />
          <select
            className="border rounded px-2 py-1 text-sm"
            value={swatchFinish}
            onChange={(e) => setSwatchFinish(e.target.value)}
          >
            {FINISHES.filter((f) => f !== "all").map((f) => (
              <option key={f} value={f}>
                {f}
              </option>
            ))}
          </select>
        </div>

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !swatchName.trim() || !swatchColor}
          onClick={() =>
            onCommitTool?.({
              tool: "PAINT_SAVE_SWATCH",
              station: "decor",
              payload: {
                name: swatchName.trim(),
                color: swatchColor,
                finish: swatchFinish,
              },
            })
          }
        >
          Save Swatch
        </button>

        <select
          className="border rounded px-2 py-1 text-sm w-full"
          value={selectedSwatchId}
          onChange={(e) => setSelectedSwatchId(e.target.value)}
        >
          <option value="">(select swatch)</option>
          {swatches.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} — {s.finish} — {s.color}
            </option>
          ))}
        </select>

        <div className="flex items-center gap-2">
          <button
            className="border rounded px-3 py-2 text-sm"
            disabled={!canEdit || !selectedId || !selectedSwatchId}
            onClick={() =>
              onCommitTool?.({
                tool: "PAINT_APPLY_SWATCH",
                station: "decor",
                payload: {
                  target_id: selectedId,
                  swatch_id: selectedSwatchId,
                },
              })
            }
          >
            Apply Swatch
          </button>

          <button
            className="border rounded px-3 py-2 text-sm"
            disabled={!canEdit || !selectedSwatchId}
            onClick={() =>
              onCommitTool?.({
                tool: "PAINT_DELETE_SWATCH",
                station: "decor",
                payload: {
                  swatch_id: selectedSwatchId,
                },
              })
            }
          >
            Delete Swatch
          </button>
        </div>
      </div>

      <div className="text-[11px] opacity-60">
        Paint presets and swatches are slot-aware if your current selection is slot-level.
      </div>
    </div>
  );
}
