// frontend/src/layout/editorLayoutState.ts

import { create } from "zustand";
import {
  DEFAULT_EDITOR_LAYOUT,
  type EditorLayoutState,
} from "./editorLayoutStore";

interface EditorLayoutStore {
  layout: EditorLayoutState;
  setLayout: (next: EditorLayoutState) => void;
}

/**
 * Runtime editor layout store.
 * Wraps the pure editor layout contract safely.
 */
export const useEditorLayoutStore = create<EditorLayoutStore>((set) => ({
  layout: DEFAULT_EDITOR_LAYOUT,
  setLayout: (next) => set({ layout: next }),
}));

