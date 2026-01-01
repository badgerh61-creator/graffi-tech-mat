// frontend/src/panels/asset-browser/useAssetPreview.ts

import { useState } from "react";
import type { EditorAsset } from "../../engine-bridge/AssetAdapter";

/**
 * H1 — Asset preview intent holder
 * Read-only, editor-safe.
 */
export function useAssetPreview() {
  const [selectedAsset, setSelectedAsset] =
    useState<EditorAsset | null>(null);

  /**
   * Engine-facing, read-only projection
   */
  const engineAsset = selectedAsset
    ? {
        id: selectedAsset.id,
        type: selectedAsset.kind,
        url: selectedAsset.previewUrl,
      }
    : undefined;

  return {
    selectedAsset,
    setSelectedAsset,
    engineAsset,
  };
}

