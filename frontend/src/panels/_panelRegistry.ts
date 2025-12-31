// src/panels/_panelRegistry.ts

import type { ComponentType } from "react";
import AssetBrowserPanel from "./asset-browser/AssetBrowserPanel";

export type PanelKey = "asset-browser";

export interface PanelDefinition {
  id: PanelKey;
  title: string;
  component: ComponentType<any>;
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
  }),
});

