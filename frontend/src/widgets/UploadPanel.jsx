// src/widgets/UploadPanel.jsx
import React, { useRef, useCallback } from "react";
import { assetsApi } from "../api";
import { useModelStore } from "../store/modelStore";
import { isAuthenticated } from "../utils/auth";

export default function UploadPanel() {
  const fetchModels = useModelStore((s) => s.fetchModels);
  const openModel = useModelStore((s) => s.openModel);
  const fileInput = useRef(null);

  const handleFile = useCallback(
    async (file) => {
      if (!file) return;

      if (!isAuthenticated()) {
        alert("You are not logged in");
        return;
      }

      try {
        const res = await assetsApi.upload(file);
        const uploaded = res.data;

        // refresh list
        await fetchModels();

        // auto-open uploaded model if backend created one
        if (uploaded?.model_id) {
          await openModel(uploaded.model_id);
        }
      } catch (err) {
        console.error("Upload failed:", err);
        alert("Upload failed");
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

