// frontend/src/services/assetService.ts

/**
 * AssetService
 *
 * Editor-facing, read-only asset access layer.
 *
 * RULES:
 * - No UI imports
 * - No engine imports
 * - No mutation
 * - No caching yet
 */

import {
  adaptEngineAsset,
  EngineAsset,
  EditorAsset,
} from "../engine-bridge/AssetAdapter";
import { getAccessToken } from "../utils/auth";

export interface AssetListResponse {
  items: EditorAsset[];
  total: number;
}

// 🔒 H1: explicit backend origin (no proxy magic)
const API_BASE = "http://localhost:8000";

export async function fetchAssets(
  page: number = 1,
  pageSize: number = 20
): Promise<AssetListResponse> {
  const token = getAccessToken();

  const res = await fetch(
    `${API_BASE}/assets/?page=${page}&pageSize=${pageSize}`,
    {
      headers: token
        ? {
            Authorization: `Bearer ${token}`,
            Accept: "application/json",
          }
        : { Accept: "application/json" },
    }
  );

  if (!res.ok) {
    throw new Error(
      `Failed to load assets (${res.status})`
    );
  }

  // 🔐 Guard against HTML responses
  const contentType =
    res.headers.get("content-type") ?? "";

  if (!contentType.includes("application/json")) {
    const text = await res.text();
    throw new Error(
      "Backend returned non-JSON response"
    );
  }

  const raw = await res.json();

  // ✅ Accept both shapes (H1-safe)
  const engineAssets: EngineAsset[] = Array.isArray(raw)
    ? raw
    : Array.isArray(raw.items)
    ? raw.items
    : [];

  return {
    items: engineAssets.map(adaptEngineAsset),
    total:
      typeof raw?.total === "number"
        ? raw.total
        : engineAssets.length,
  };
}

