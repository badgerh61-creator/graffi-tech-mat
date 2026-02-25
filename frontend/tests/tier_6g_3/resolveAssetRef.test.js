// frontend/tests/tier_6g_3/resolveAssetRef.test.js
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { resolveAssetRef } from "../../src/editor/scene/resolveAssetRef";

describe("resolveAssetRef", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.resetAllMocks();
  });

  it("passes through absolute urls", async () => {
    const url = await resolveAssetRef("https://example.com/a.glb");
    expect(url).toBe("https://example.com/a.glb");
  });

  it("passes through relative paths", async () => {
    const url = await resolveAssetRef("/vehicles/a.glb");
    expect(url).toBe("/vehicles/a.glb");
  });

  it("resolves asset:<id> via /assets/<id>/url", async () => {
    globalThis.fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ url: "https://signed.example.com/x.glb", type: "glb" }),
    });

    const url = await resolveAssetRef("asset:123");
    expect(globalThis.fetch).toHaveBeenCalledWith("http://127.0.0.1:8000/assets/123/url");
    expect(url).toBe("https://signed.example.com/x.glb");
  });
});
