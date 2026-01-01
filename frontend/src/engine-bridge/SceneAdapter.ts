// frontend/src/engine-bridge/SceneAdapter.ts

/**
 * SceneAdapter (PREVIEW-ONLY)
 *
 * Editor → Engine bridge for read-only scene preview.
 *
 * RULES:
 * - No engine internals imported
 * - No mutation
 * - No serialization
 * - No persistence
 */

export interface ScenePreviewDescriptor {
  assetId: string;
  assetType: "model" | "image";
  cameraPreset?: "default" | "close" | "wide";
  lightingPreset?: "studio" | "neutral";
}

/**
 * Attach a preview asset to the engine scene.
 * This MUST be deterministic and reversible.
 */
export function previewAssetInScene(
  descriptor: ScenePreviewDescriptor
): void {
  /**
   * NOTE:
   * This function intentionally delegates to the engine bridge
   * without exposing engine state or accepting scene objects.
   *
   * Implementation is opaque by design.
   */
  window.dispatchEvent(
    new CustomEvent("engine:preview-asset", {
      detail: descriptor,
    })
  );
}

/**
 * Clear preview scene safely.
 */
export function clearScenePreview(): void {
  window.dispatchEvent(
    new CustomEvent("engine:clear-preview")
  );
}

