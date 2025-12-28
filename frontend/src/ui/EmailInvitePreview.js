// src/ui/EmailInvitePreview.jsx
import React from "react";
import { timeAgo } from "../utils/time";

export default function EmailInvitePreview({
  modelName,
  role,
  inviterEmail,
  expiresAt,
  onClose,
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/40"
        onClick={onClose}
      />

      <div className="relative bg-white rounded-lg shadow-xl max-w-lg w-full mx-4">
        <div className="px-4 py-3 border-b flex justify-between">
          <div className="font-semibold text-sm">
            Email preview
          </div>
          <button onClick={onClose}>✕</button>
        </div>

        <div className="p-5 text-sm space-y-4">
          <div className="text-xs text-slate-400">
            Subject
          </div>

          <div className="font-medium">
            You’ve been invited to collaborate on {modelName}
          </div>

          <hr />

          <p>
            {inviterEmail ?? "A collaborator"} invited you as a{" "}
            <strong className="capitalize">{role}</strong>.
          </p>

          <p>
            This invite expires{" "}
            <strong>
              {expiresAt ? timeAgo(expiresAt) : "in 7 days"}
            </strong>.
          </p>

          <button
            className="px-4 py-2 bg-slate-800 text-white rounded text-sm"
            disabled
          >
            Accept invitation
          </button>

          <p className="text-xs text-slate-400">
            Preview only — no email sent.
          </p>
        </div>
      </div>
    </div>
  );
}

