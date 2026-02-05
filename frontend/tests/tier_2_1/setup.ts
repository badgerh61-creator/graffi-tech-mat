// tests/tier_2_1/setup.ts
import * as harness from "./testHarness"
import "@testing-library/jest-dom"

// Expose helpers globally
Object.assign(globalThis, harness)

// ✅ Render a default editor before each test
beforeEach(() => {
  harness.renderEditor()
})

