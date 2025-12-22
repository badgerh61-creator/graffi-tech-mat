// src/widgets/UploadPanel.jsx
import React, { useRef, useCallback } from "react";
import { useModelStore } from "../store/modelStore";

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export default function UploadPanel() {
  const fetchModels = useModelStore((s) => s.fetchModels);
  const openModel = useModelStore((s) => s.openModel);
  const fileInput = useRef(null);

  const handleFile = useCallback(
    async (file) => {
      if (!file) return;

      const token = localStorage.getItem("access_token");
      if (!token) {
        alert("Not authenticated");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/upload/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) {
        console.error("Upload failed");
        alert("Upload failed");
        return;
      }

      const uploaded = await res.json();

      // 🔑 refresh list
      await fetchModels();

      // 🔑 AUTO-OPEN uploaded model (THIS WAS MISSING)
      if (uploaded.model_id) {
        await openModel(uploaded.model_id);
      }
    },
    [fetchModels, openModel]
  );

  return (
    <div className="flex items-center gap-3">
      <button
        type="button"
        className="btn-sm"
        onClick={() => fileInput.current?.click()}
      >
        Upload GLB
      </button>

      <input
        ref={fileInput}
        type="file"
        accept=".glb,.gltf"
        className="hidden"
        onChange={(e) => {
          handleFile(e.target.files?.[0]);
          e.target.value = "";
        }}
      />
    </div>
  );
}

