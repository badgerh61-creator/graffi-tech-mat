// frontend/src/services/studio/modelAssetsApi.js
import { listAssets } from "./assetsApi";

/**
 * fetchModelAssets()
 * Thin adapter for ModelAssetPickerPanel.
 * Normalizes /assets/ response { items, total } -> items[]
 */
export async function fetchModelAssets() {
  const data = await listAssets();
  return Array.isArray(data?.items) ? data.items : [];
}
