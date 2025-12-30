export type AssetType = "image" | "model" | "vector" | "other";

export interface Asset {
  id: string;
  name: string;
  type: AssetType;
  url: string;
  thumbnailUrl?: string;
  tags?: string[];
}

