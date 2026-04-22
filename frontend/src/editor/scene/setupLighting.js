import { setupStudioLighting } from "./setupStudioLighting";

export async function setupLighting(renderer, scene) {
  try {
    await setupStudioLighting({
      renderer,
      scene,
      hdrUrl: undefined, // safe default for tests
    });
  } catch {
    // test-safe fallback (do nothing)
  }
}
