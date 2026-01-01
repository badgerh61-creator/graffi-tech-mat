// frontend/src/panels/asset-browser/useAssetPreview.ts

import { useState, useEffect } from "react";
import type { EditorAsset } from "../../engine-bridge/AssetAdapter";
import {
  previewAssetInScene,
  clearScenePreview,
} from "../../engine-bridge/SceneAdapter";

/**
 * Asset preview hook
 *
 * RULES:
 * - Selection is editor state
 * - Preview is engine side-effect
 * - No persistence
 * - No mutation
 */
export function useAssetPreview() {
  const [selectedAsset, setSelectedAsset] =
    useState<EditorAsset | null>(null);

  /**
   * 🔗 Phase H2 — bridge selection → engine preview
   */
  useEffect(() => {
    if (!selectedAsset) {
      clearScenePreview();
      return;
    }

    previewAssetInScene({
      assetId: selectedAsset.id,
      assetType: selectedAsset.type,
      cameraPreset: "default",
      lightingPreset: "studio",
    });
  }, [selectedAsset]);

  return {
    selectedAsset,
    setSelectedAsset,
  };
}

