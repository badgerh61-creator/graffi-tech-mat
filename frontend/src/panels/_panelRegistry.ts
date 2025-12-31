// src/panels/_panelRegistry.ts

import type { ComponentType } from "react";

import AssetBrowserPanel from "./asset-browser/AssetBrowserPanel";

export type PanelKey =
  | "asset-browser";

export interface PanelDefinition {
  id: PanelKey;
  title: string;
  component: ComponentType<any>;
}

export const panelRegistry: Record<PanelKey, PanelDefinition> = {
  "asset-browser": {
    id: "asset-browser",
    title: "Assets",
    component: AssetBrowserPanel,
  },
};

