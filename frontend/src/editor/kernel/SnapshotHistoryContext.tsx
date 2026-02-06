import { createContext, useContext } from "react";

export const SnapshotHistoryContext = createContext(null);

export function useSnapshotHistory() {
  const ctx = useContext(SnapshotHistoryContext);

  if (!ctx) {
    return {
      history: [],
      activeSnapshotId: null,
      navigateTo: () => {},
    };
  }

  return ctx;
}

