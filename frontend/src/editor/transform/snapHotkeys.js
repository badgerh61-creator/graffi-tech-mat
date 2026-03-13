import { setSnap } from "./snapStore";

export function handleSnapHotkey(event) {
  const key = String(event.key || "").toLowerCase();

  if (key === "x") {
    setSnap({ axis_lock: "x" });
    return true;
  }
  if (key === "y") {
    setSnap({ axis_lock: "y" });
    return true;
  }
  if (key === "z") {
    setSnap({ axis_lock: "z" });
    return true;
  }
  if (key === "escape") {
    setSnap({ axis_lock: "none" });
    return true;
  }
  return false;
}
