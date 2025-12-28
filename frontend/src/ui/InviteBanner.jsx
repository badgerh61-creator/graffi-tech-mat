// src/ui/InviteBanner.jsx
import React from "react";

const DISMISS_KEY = "invite_banner_dismissed";

export default function InviteBanner({ role, onDismiss }) {
  if (localStorage.getItem(DISMISS_KEY)) return null;

  function dismiss() {
    localStorage.setItem(DISMISS_KEY, "1");
    onDismiss?.();
  }

  return (
    <div className="bg-blue-50 border-b border-blue-200 px-4 py-2 text-sm flex items-center justify-between">
      <div>
        You were invited as{" "}
        <strong className="capitalize">{role}</strong>
      </div>

      <button
        onClick={dismiss}
        className="text-blue-700 hover:underline text-xs"
      >
        Dismiss
      </button>
    </div>
  );
}

