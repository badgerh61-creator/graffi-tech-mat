import { describe, it, expect } from "vitest";
import { assetUriToUrl } from "../../src/editor/scene/assetUriToUrl";

describe("Tier 6G.13 — assetUriToUrl", () => {
  it("converts asset ref to API endpoint", () => {
    const url = assetUriToUrl("asset:123");

    expect(url).toContain("/assets/123/url");
  });

  it("returns null for null input", () => {
    expect(assetUriToUrl(null)).toBe(null);
  });
});
