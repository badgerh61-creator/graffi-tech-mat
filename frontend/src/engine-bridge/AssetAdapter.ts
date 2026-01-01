// frontend/src/engine-bridge/AssetAdapter.ts

/**
 * AssetAdapter
 *
 * Translates backend/engine asset records
 * into editor-safe, deterministic assets.
 *
 * H1 RULES:
 * - Read-only
 * - No engine side effects
 * - No preview loading yet
 */

export interface EngineAsset {
  id: number;
  filename: string;
  content_type?: string;
  status?: string;
}

export interface EditorAsset {
  id: string;
  name: string;
  kind: "model" | "image" | "unknown";
}

/**
 * Adapt backend asset → editor asset
 */
export function adaptEngineAsset(
  asset: EngineAsset
): EditorAsset {
  const filename = asset.filename ?? "Unnamed";

  let kind: EditorAsset["kind"] = "unknown";

  if (filename.toLowerCase().endsWith(".glb")) {
    kind = "model";
  } else if (
    filename.match(/\.(png|jpg|jpeg|webp)$/i)
  ) {
    kind = "image";
  }

  return {
    id: String(asset.id),
    name: filename,
    kind,
  };
}

