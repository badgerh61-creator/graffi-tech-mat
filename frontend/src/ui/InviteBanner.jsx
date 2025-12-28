// src/ui/InviteBanner.jsx

import React from "react";
import InviteExpiry from "./InviteExpiry";

export default function InviteBanner({ role, createdAt, onDismiss }) {
  return (
    <div className="bg-indigo-50 border-b border-indigo-200 px-4 py-3 text-sm flex items-center justify-between gap-3">
      <div className="flex flex-col gap-1">
        <div className="text-indigo-900">
          You were invited as{" "}
          <strong>{role}</strong>
        </div>

        <InviteExpiry createdAt={createdAt} />
      </div>

      <button
        onClick={onDismiss}
        className="text-xs text-indigo-700 hover:underline"
      >
        Dismiss
      </button>
    </div>
  );
}

