// src/ui/StudioTabs.jsx
import React from "react";
import { useStudioTabsStore } from "../store/studioTabsStore";

export default function StudioTabs() {
  const tabs = useStudioTabsStore((s) => s.tabs);
  const active = useStudioTabsStore((s) => s.active);
  const setActive = useStudioTabsStore((s) => s.setActive);
  const addTab = useStudioTabsStore((s) => s.addTab);

  return (
    <div className="flex items-center gap-2">
      {tabs.map((t) => (
        <div
          key={t}
          className={`px-3 py-1 rounded-md ${
            t === active ? "bg-ui-surface shadow card-shadow" : "bg-ui-surface/60"
          }`}
        >
          <button onClick={() => setActive(t)} className="text-sm capitalize">
            {t}
          </button>
        </div>
      ))}

      <button
        className="ml-4 text-sm btn-sm"
        onClick={() => addTab("tab-" + Math.random().toString(36).slice(2, 6))}
      >
        + New
      </button>
    </div>
  );
}
