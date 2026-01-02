// frontend/src/layout/defaultEditorLayout.ts

import { EditorLayoutState } from "./editorLayout.types";

/**
 * Default editor layout (Phase G / H)
 * Pure structural intent — no logic, no permissions.
 */
export const DEFAULT_EDITOR_LAYOUT: EditorLayoutState = {
  left: ["asset-browser"],
  right: ["engine-preview"],
  bottom: ["jobs"], // ✅ Phase H3
  center: "workspace",
};

