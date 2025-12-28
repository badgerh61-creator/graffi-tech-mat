// src/ui/ActivityFeed.jsx

import React, { useEffect, useState } from "react";
import { activityApi } from "../api/activity";

export default function ActivityFeed() {
  const [items, setItems] = useState([]);
  const [status, setStatus] = useState("loading"); 
  // loading | ready | empty | unavailable

  useEffect(() => {
    let cancelled = false;

    async function loadActivity() {
      try {
        const res = await activityApi.list({ page: 1, limit: 50 });
        if (cancelled) return;

        if (Array.isArray(res.data) && res.data.length > 0) {
          setItems(res.data);
          setStatus("ready");
        } else {
          setStatus("empty");
        }
      } catch (err) {
        // 🔒 IMPORTANT: 404 = backend not implemented (expected)
        if (err?.response?.status === 404) {
          setStatus("unavailable");
          return;
        }

        // Any other error → fail closed but silent
        setStatus("unavailable");
      }
    }

    loadActivity();

    return () => {
      cancelled = true;
    };
  }, []);

  // 🔵 LOADING STATE
  if (status === "loading") {
    return (
      <div className="text-xs text-slate-400">
        Loading activity…
      </div>
    );
  }

  // 🔵 BACKEND NOT AVAILABLE (EXPECTED)
  if (status === "unavailable") {
    return (
      <div className="text-xs text-slate-400">
        Activity coming soon.
      </div>
    );
  }

  // 🔵 EMPTY BUT WORKING
  if (status === "empty") {
    return (
      <div className="text-xs text-slate-400">
        No recent activity yet.
      </div>
    );
  }

  // 🔵 NORMAL RENDER
  return (
    <ul className="space-y-2 text-sm">
      {items.map((item) => (
        <li
          key={item.id}
          className="border-b last:border-b-0 pb-1"
        >
          {item.message}
        </li>
      ))}
    </ul>
  );
}

