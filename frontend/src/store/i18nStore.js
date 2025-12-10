// frontend/src/store/i18nStore.js
import { create } from "zustand";

export const useI18nStore = create((set, get) => ({
  lang: "en",
  strings: {},

  setLang: (lang) => set({ lang }),

  loadStrings: (strings) => set({ strings }),

  t: (key) => {
    const s = get().strings;
    return s && s[key] ? s[key] : key;
  },
}));
