// src/widgets/UploadPanel.jsx
import React, { useRef, useCallback } from "react";
import { useAssetStore } from "../store/assetStore";
import { useModelStore } from "../store/modelStore";

export default function UploadPanel({ onUploaded }) {
  const addAsset = useAssetStore((s) => s.addAssetFromFile);
  const addModelFromAsset = useModelStore((s) => s.addModelFromAsset);

  const fileInput = useRef(null);

  const handleFile = useCallback(
    async (file) => {
      if (!file) return;
      const asset = await addAsset(file);

      if (asset.type === "model") {
        addModelFromAsset(asset);
      }

      onUploaded && onUploaded(asset);
    },
    [addAsset, addModelFromAsset, onUploaded]
  );

  return (
    <div className="flex items-center gap-3">
      <button className="btn-sm" onClick={() => fileInput.current.click()}>
        Browse
      </button>

      <span className="text-xs text-gray-400">
        Drag & drop images, HDRIs, GLB, FBX, OBJ, ZIP.
      </span>

      <input
        ref={fileInput}
        type="file"
        className="hidden"
        accept=".gltf,.glb,.obj,.fbx,.hdr,.exr,.zip,image/*"
        onChange={(e) => {
          const file = e.target.files?.[0];
          handleFile(file);
          e.target.value = "";
        }}
      />
    </div>
  );
}
