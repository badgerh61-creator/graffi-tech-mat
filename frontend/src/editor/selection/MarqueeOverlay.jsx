import React from "react";
import { useSyncExternalStore } from "react";
import { marqueeSubscribe, marqueeGetSnapshot } from "./marqueeStore";

function useMarquee() {
  return useSyncExternalStore(
    marqueeSubscribe,
    marqueeGetSnapshot,
    marqueeGetSnapshot
  );
}

function rectFromPoints(a, b) {
  if (!a || !b) return null;

  const x1 = Math.min(a.x, b.x);
  const y1 = Math.min(a.y, b.y);
  const x2 = Math.max(a.x, b.x);
  const y2 = Math.max(a.y, b.y);

  return {
    left: x1,
    top: y1,
    width: x2 - x1,
    height: y2 - y1,
  };
}

export default function MarqueeOverlay() {
  const { active, start, end } = useMarquee();

  if (!active) return null;

  const rect = rectFromPoints(start, end);
  if (!rect) return null;

  return (
    <div
      style={{
        position: "absolute",
        pointerEvents: "none",
        left: rect.left,
        top: rect.top,
        width: rect.width,
        height: rect.height,
        border: "1px dashed #3b82f6",
        background: "rgba(59,130,246,0.1)",
        zIndex: 1000,
      }}
    />
  );
}
