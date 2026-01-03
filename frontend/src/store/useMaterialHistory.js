// src/useMaterialHistory.js

import { useCallback, useState } from "react";

/**
 * Phase G compliant material history hook.
 * Logic ONLY — no UI, no layout.
 */
export default function useMaterialHistory() {
  const [history, setHistory] = useState([]);
  const [cursor, setCursor] = useState(-1);

  const push = useCallback((entry) => {
    setHistory((prev) => {
      const next = prev.slice(0, cursor + 1);
      next.push(entry);
      return next;
    });
    setCursor((c) => c + 1);
  }, [cursor]);

  const undo = useCallback(() => {
    setCursor((c) => Math.max(c - 1, -1));
  }, []);

  const redo = useCallback(() => {
    setCursor((c) => Math.min(c + 1, history.length - 1));
  }, [history.length]);

  return {
    history,
    cursor,
    canUndo: cursor >= 0,
    canRedo: cursor < history.length - 1,
    push,
    undo,
    redo,
  };
}

