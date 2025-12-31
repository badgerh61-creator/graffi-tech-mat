// src/panels/_panelRegistry.ts

import type { ComponentType } from "react";
import AssetBrowserPanel from "./asset-browser/AssetBrowserPanel";

export type PanelKey = "asset-browser";

export type PanelCapability =
  | "assets.view"
  | "assets.use";

export interface PanelDefinition {
  id: PanelKey;
  title: string;
  component: ComponentType<any>;

  /**
   * Capability required to render this panel.
   * Enforcement happens inside the panel itself.
   */
  requiredCapability: PanelCapability;
}

/**
 * Panel registry is immutable by design.
 * Panels must be registered at build-time, not runtime.
 */
export const panelRegistry = Object.freeze<
  Readonly<Record<PanelKey, PanelDefinition>>
>({
  "asset-browser": Object.freeze({
    id: "asset-browser",
    title: "Assets",
    component: AssetBrowserPanel,

    // Week 7 metadata (NO enforcement yet)
    requiredCapability: "assets.view",
  }),
});

