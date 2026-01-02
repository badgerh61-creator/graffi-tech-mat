// frontend/src/panels/engine-preview/EnginePreviewPanel.tsx

import EnginePreview from "../../engine/EnginePreview";
import { useAssetPreview } from "../asset-browser/useAssetPreview";

export function EnginePreviewPanel() {
  const { selectedAsset } = useAssetPreview();

  return (
    <div className="engine-preview-panel">
      <EnginePreview asset={selectedAsset} />
    </div>
  );
}

