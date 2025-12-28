// src/ui/InviteExpiry.jsx
import React from "react";

export default function InviteExpiry({ expiresAt }) {
  if (!expiresAt) return null;

  const ms = new Date(expiresAt).getTime() - Date.now();
  const hours = Math.max(0, Math.floor(ms / 3600000));

  return (
    <span className="text-xs text-slate-500">
      expires in {hours}h
    </span>
  );
}

