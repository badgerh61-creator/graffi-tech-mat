import { useEffect } from "react";
import { SHORTCUTS } from "./shortcutRegistry";

function isTypingTarget(el) {
  if (!el) return false;
  const tag = el.tagName?.toLowerCase();
  return tag === "input" || tag === "textarea" || el.isContentEditable;
}

function matchShortcut(e, s) {
  if (s.key !== e.key.toLowerCase()) return false;
  if (!!s.ctrl !== (e.ctrlKey || e.metaKey)) return false;
  if (!!s.shift !== e.shiftKey) return false;
  return true;
}

export function useKeyboardShortcuts({
  onAction,
}) {
  useEffect(() => {
    function handle(e) {
      if (isTypingTarget(e.target)) return;

      for (const s of SHORTCUTS) {
        if (matchShortcut(e, s)) {
          e.preventDefault();
          onAction?.(s.action);
          return;
        }
      }
    }

    window.addEventListener("keydown", handle);
    return () => window.removeEventListener("keydown", handle);
  }, [onAction]);
}
