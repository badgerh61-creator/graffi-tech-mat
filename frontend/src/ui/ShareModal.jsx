// src/ui/ShareModal.jsx
import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import { useModelStore } from "../store/modelStore";
import { getAccessToken } from "../utils/auth";
import { timeAgo } from "../utils/time";

/* ---------------- JWT HELPERS ---------------- */
function decodeJwt(token) {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
}

export default function ShareModal({ modelId, onClose }) {
  const permissions = useModelStore((s) => s.modelPermissions);

  const token = getAccessToken();
  const currentUser = token ? decodeJwt(token) : null;
  const currentUserId = currentUser?.sub ?? null;
  const currentUserEmail = currentUser?.email ?? null;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [collaborators, setCollaborators] = useState([]);
  const [invites, setInvites] = useState([]);

  const [email, setEmail] = useState("");
  const [role, setRole] = useState("viewer");

  /* ---------------- ESC CLOSE ---------------- */
  useEffect(() => {
    function onKey(e) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  /* ---------------- LOAD DATA ---------------- */
  useEffect(() => {
    if (!modelId) return;
    loadAll();
  }, [modelId]);

  async function loadAll() {
    setLoading(true);
    setError(null);

    try {
      const [collabRes, inviteRes] = await Promise.all([
        api.get(`/models/${modelId}/collaborators`),
        api.get(`/models/${modelId}/invites`),
      ]);

      setCollaborators(collabRes.data ?? []);
      setInvites(inviteRes.data ?? []);
    } catch {
      setError("Failed to load sharing information");
    } finally {
      setLoading(false);
    }
  }

  /* ---------------- INVITES ---------------- */
  async function sendInvite() {
    if (!email) return;

    try {
      await api.post(`/models/${modelId}/invites`, null, {
        params: { email, role },
      });
      setEmail("");
      setRole("viewer");
      loadAll();
    } catch {
      setError("Failed to send invite");
    }
  }

  async function revokeInvite(inviteId) {
    if (!confirm("Revoke this invite?")) return;

    try {
      await api.delete(`/models/invites/${inviteId}`);
      loadAll();
    } catch {
      setError("Failed to revoke invite");
    }
  }

  async function changeRole(userId, newRole) {
    try {
      await api.patch(
        `/models/${modelId}/collaborators/${userId}`,
        { role: newRole }
      );
      loadAll();
    } catch {
      setError("Failed to update role");
    }
  }

  async function removeCollaborator(userId) {
    if (!confirm("Remove collaborator?")) return;

    try {
      await api.delete(`/models/${modelId}/collaborators/${userId}`);
      loadAll();
    } catch {
      setError("Failed to remove collaborator");
    }
  }

  if (!modelId) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />

      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 overflow-hidden">
        <div className="flex items-center justify-between px-4 py-3 border-b">
          <div className="font-semibold text-sm">Share model</div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
            ✕
          </button>
        </div>

        <div className="p-4 space-y-5 text-sm">
          {loading && <div className="text-xs text-slate-400">Loading…</div>}
          {error && <div className="text-xs text-rose-600">{error}</div>}

          <div className="text-xs text-slate-500 bg-slate-50 border rounded p-2">
            Owners control access. Editors can invite and edit. Viewers have read-only access.
          </div>

          {/* COLLABORATORS */}
          <div className="space-y-2">
            <div className="font-medium text-slate-700">Collaborators</div>

            {collaborators.length === 0 && (
              <div className="text-xs text-slate-400">No collaborators</div>
            )}

            {collaborators.map((c) => {
              const isOwner = c.role === "owner";
              const isYou = c.user_id === currentUserId;

              const label =
                c.email ??
                (isYou ? currentUserEmail : `User #${c.user_id}`);

              return (
                <div key={c.user_id} className="flex items-center justify-between">
                  <div className="truncate">
                    {label}
                    {isYou && <span className="ml-1 text-xs text-slate-400">(You)</span>}
                  </div>

                  {isOwner ? (
                    <span className="px-2 py-0.5 rounded text-xs bg-slate-200">
                      Owner
                    </span>
                  ) : (
                    <div className="flex items-center gap-2">
                      <select
                        value={c.role}
                        onChange={(e) => changeRole(c.user_id, e.target.value)}
                        disabled={!permissions.canEdit}
                        className="text-xs border rounded px-1 py-0.5 disabled:opacity-60"
                      >
                        <option value="viewer">viewer</option>
                        <option value="editor">editor</option>
                      </select>

                      <button
                        onClick={() => removeCollaborator(c.user_id)}
                        disabled={!permissions.canDelete}
                        className="text-xs text-rose-600 disabled:text-slate-400"
                      >
                        Remove
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* INVITES */}
          <div className="space-y-2">
            <div className="font-medium text-slate-700">Pending invites</div>

            {invites.length === 0 && (
              <div className="text-xs text-slate-400">
                No pending invites
              </div>
            )}

            {invites.map((i) => (
              <div key={i.id} className="flex items-center justify-between">
                <div>
                  {i.email}
                  <div className="text-xs text-slate-400">
                    sent {timeAgo(i.created_at)}
                  </div>
                </div>

                <button
                  onClick={() => revokeInvite(i.id)}
                  disabled={!permissions.canDelete}
                  className="text-xs text-rose-600 disabled:text-slate-400"
                >
                  Revoke
                </button>
              </div>
            ))}
          </div>

          {/* SEND INVITE */}
          {permissions.canEdit ? (
            <div className="pt-3 border-t space-y-2">
              <div className="font-medium text-slate-700">Invite by email</div>

              <input
                type="email"
                placeholder="user@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-2 py-1 border rounded text-sm"
              />

              <div className="flex gap-2">
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="flex-1 px-2 py-1 border rounded text-sm"
                >
                  <option value="viewer">viewer</option>
                  <option value="editor">editor</option>
                </select>

                <button
                  onClick={sendInvite}
                  disabled={!email}
                  className="btn-sm disabled:opacity-50"
                >
                  Send invite
                </button>
              </div>
            </div>
          ) : (
            <div className="pt-3 border-t text-xs text-slate-400">
              Only editors or owners can invite collaborators.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

