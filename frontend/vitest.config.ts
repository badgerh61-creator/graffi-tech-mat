// vitest.config.ts
import { defineConfig } from "vitest/config"
import path from "path"

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  test: {
    environment: "jsdom", // ✅ REQUIRED
    globals: true, 
    setupFiles:[
    "./tests/setupTests.ts",  
    "./tests/tier_2_1/setup.ts"],
  },
})

