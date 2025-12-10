// src/store/cameraBookmarksStore.js
import { create } from "zustand";
import { nanoid } from "nanoid";

export const useCameraBookmarksStore = create((set, get) => ({
  bookmarks: [],

  addBookmark(name = "View") {
    const id = nanoid();
    set((s) => ({
      bookmarks: [
        { id, name, cameraState: null, createdAt: Date.now() },
        ...s.bookmarks,
      ],
    }));
    return id;
  },

  updateBookmarkState(id, cameraState) {
    set((s) => ({
      bookmarks: s.bookmarks.map((b) =>
        b.id === id ? { ...b, cameraState } : b
      ),
    }));
  },

  removeBookmark(id) {
    set((s) => ({
      bookmarks: s.bookmarks.filter((b) => b.id !== id),
    }));
  },
}));
