// src/ui/InviteExpiry.jsx

import React from "react";

const INVITE_LIFETIME_DAYS = 7;

export default function InviteExpiry({ createdAt }) {
  if (!createdAt) {
    return (
      <span className="text-xs text-slate-500">
        Expiry unknown
      </span>
    );
  }

  const created = new Date(createdAt).getTime();
  const expiresAt =
    created + INVITE_LIFETIME_DAYS * 24 * 60 * 60 * 1000;

  const now = Date.now();
  const remainingMs = expiresAt - now;

  if (remainingMs <= 0) {
    return (
      <span className="text-xs text-rose-600">
        Invite expired
      </span>
    );
  }

  const days = Math.ceil(remainingMs / (24 * 60 * 60 * 1000));

  return (
    <span className="text-xs text-slate-500">
      Expires in {days} day{days !== 1 ? "s" : ""}
    </span>
  );
}

