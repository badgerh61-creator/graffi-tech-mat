// frontend/src/panels/_panelRegistry.ts

import type { ComponentType } from "react";

import AssetBrowserPanel from "./asset-browser/AssetBrowserPanel";
import { EnginePreviewPanel } from "./engine-preview/EnginePreviewPanel";
import JobPanel from "./jobs/JobPanel";
import EngineeringAssistantPanel from "../editor/panels/engineering/EngineeringAssistantPanel";

// ✅ NEW dock panels
import HistoryPanel from "../editor/panels/HistoryPanel";
import ConstraintPanel from "../editor/panels/ConstraintPanel";

export type PanelKey =
  | "asset-browser"
  | "engine-preview"
  | "jobs"
  | "engineering-assistant"
  | "history"
  | "constraints";

export type PanelCapability =
  | "assets.view"
  | "assets.use"
  | "engine.preview"
  | "jobs.view"
  | "engineering.assistant.use"
  | "history.view"
  | "constraints.view";

export interface PanelDefinition {
  id: PanelKey;
  title: string;
  component: ComponentType<any>;
  requiredCapability: PanelCapability;
}

export const panelRegistry = Object.freeze<
  Readonly<Record<PanelKey, PanelDefinition>>
>({
  "asset-browser": Object.freeze({
    id: "asset-browser",
    title: "Assets",
    component: AssetBrowserPanel,
    requiredCapability: "assets.view",
  }),

  "engine-preview": Object.freeze({
    id: "engine-preview",
    title: "Preview",
    component: EnginePreviewPanel,
    requiredCapability: "engine.preview",
  }),

  jobs: Object.freeze({
    id: "jobs",
    title: "Jobs",
    component: JobPanel,
    requiredCapability: "jobs.view",
  }),

  "engineering-assistant": Object.freeze({
    id: "engineering-assistant",
    title: "Engineering Assistant",
    component: EngineeringAssistantPanel,
    requiredCapability: "engineering.assistant.use",
  }),

  history: Object.freeze({
    id: "history",
    title: "History",
    component: HistoryPanel,
    requiredCapability: "history.view",
  }),

  constraints: Object.freeze({
    id: "constraints",
    title: "Constraints",
    component: ConstraintPanel,
    requiredCapability: "constraints.view",
  }),
});
