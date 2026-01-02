// src/panels/_panelRegistry.ts

import type { ComponentType } from "react";
import AssetBrowserPanel from "./asset-browser/AssetBrowserPanel";
import { EnginePreviewPanel } from "./engine-preview/EnginePreviewPanel";
import JobPanel from "./jobs/JobPanel";

/**
 * Panel keys must be declared explicitly.
 * This is intentional — no dynamic injection.
 */
export type PanelKey =
  | "asset-browser"
  | "engine-preview"
  | "jobs";

export type PanelCapability =
  | "assets.view"
  | "assets.use"
  | "engine.preview"
  | "jobs.view";

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

    // Phase G / H — view-only
    requiredCapability: "assets.view",
  }),

  "engine-preview": Object.freeze({
    id: "engine-preview",
    title: "Preview",
    component: EnginePreviewPanel,

    // Phase H — read-only engine visibility
    requiredCapability: "engine.preview",
  }),

  "jobs": Object.freeze({
    id: "jobs",
    title: "Jobs",
    component: JobPanel,

    // Phase H3 — async job visibility only
    requiredCapability: "jobs.view",
  }),
});

