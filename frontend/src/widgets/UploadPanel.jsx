// frontend/src/widgets/UploadPanel.jsx

import React, { useRef, useCallback, useState } from "react";
import { assetsApi } from "../api";
import { useModelStore } from "../store/modelStore";
import { isAuthenticated } from "../utils/auth";

export default function UploadPanel() {
  const fetchModels = useModelStore((s) => s.fetchModels);
  const openModel = useModelStore((s) => s.openModel);
  const permissions = useModelStore((s) => s.modelPermissions);
  const modelStatus = useModelStore((s) => s.modelStatus);

  // ✅ ACTIVE MODEL ID (THIS WAS MISSING)
  const activeModelId = useModelStore((s) => s.activeModelId);

  const fileInput = useRef(null);
  const [uploading, setUploading] = useState(false);

  const handleFile = useCallback(
    async (file) => {
      if (!file || uploading) return;
      if (!permissions.canUpload) return;

      if (!isAuthenticated()) {
        alert("You are not logged in");
        return;
      }

      if (!activeModelId) {
        alert("No active model selected");
        return;
      }

      setUploading(true);

      try {
        // ✅ FIXED: model_id is now sent
        const res = await assetsApi.upload(file, activeModelId);
        const uploaded = res.data;

        await fetchModels();

        if (uploaded?.model_id) {
          await openModel(uploaded.model_id);
        }
      } catch (err) {
        console.error("Upload failed:", err);
        alert("Upload failed. Please retry.");
      } finally {
        setUploading(false);
      }
    },
    [
      uploading,
      permissions.canUpload,
      activeModelId,
      fetchModels,
      openModel,
    ]
  );

  if (!permissions.canUpload) {
    return <div className="text-sm text-slate-400">Read-only access</div>;
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-3">
        <button
          type="button"
          className="btn-sm disabled:opacity-60"
          disabled={uploading}
          onClick={() => fileInput.current?.click()}
        >
          {uploading ? "Uploading…" : "Upload GLB"}
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

      {modelStatus === "loading" && (
        <div className="text-xs text-slate-500">
          Processing model…
        </div>
      )}

      {modelStatus === "failed" && (
        <div className="text-xs text-rose-600">
          Processing failed. You can retry upload.
        </div>
      )}
    </div>
  );
}

