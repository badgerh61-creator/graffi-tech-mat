import { EnginePreview } from "../../engine/EnginePreview";
import { useAssetPreview } from "../asset-browser/useAssetPreview";

export function EnginePreviewPanel() {
  const { engineAsset } = useAssetPreview();

  if (!engineAsset) {
    return <div>No asset selected</div>;
  }

  return <EnginePreview asset={engineAsset} />;
}

