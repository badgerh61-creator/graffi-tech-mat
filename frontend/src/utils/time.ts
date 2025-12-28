// src/utils/time.ts

export function timeAgo(date: string | Date): string {
  const ts = new Date(date).getTime();
  if (Number.isNaN(ts)) return "";

  const seconds = Math.floor((Date.now() - ts) / 1000);

  if (seconds < 60) return "just now";
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

