import React, { useEffect, useState } from "react";
import { adminApi } from "../api/admin";
import { normalizeApiError } from "../api/errors";
import AdminUserTable from "../ui/Admin/User/Table";
import AdminAudit from "./AdminAudit";

export default function Admin() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);
  const [tab, setTab] = useState("users");

  /* ================= LOADERS ================= */

  async function loadUsers() {
    try {
      setError(null);
      const res = await adminApi.listUsers();
      setUsers(res.data);
    } catch (err) {
      setError(normalizeApiError(err));
    }
  }

  /* ================= EFFECTS ================= */

  useEffect(() => {
    if (tab === "users") {
      loadUsers();
    } else {
      setError(null); // clear stale errors when switching tabs
    }
  }, [tab]);

  /* ================= ACTIONS ================= */

  async function changeRole(id, role) {
    try {
      await adminApi.setUserRole(id, role);
      loadUsers();
    } catch (err) {
      setError(normalizeApiError(err));
    }
  }

  async function toggleActive(id, active) {
    try {
      await adminApi.setUserActive(id, active);
      loadUsers();
    } catch (err) {
      setError(normalizeApiError(err));
    }
  }

  async function revoke(id) {
    try {
      await adminApi.revokeSessions(id);
      alert("Sessions revoked");
    } catch (err) {
      setError(normalizeApiError(err));
    }
  }

  /* ================= RENDER ================= */

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">
        Admin Panel
      </h1>

      {/* ---------- TABS ---------- */}
      <div className="flex gap-4 text-sm border-b pb-2">
        <button
          onClick={() => setTab("users")}
          className={`pb-1 ${
            tab === "users"
              ? "font-semibold border-b-2 border-black"
              : "text-slate-500"
          }`}
        >
          Users
        </button>

        <button
          onClick={() => setTab("audit")}
          className={`pb-1 ${
            tab === "audit"
              ? "font-semibold border-b-2 border-black"
              : "text-slate-500"
          }`}
        >
          Audit Log
        </button>
      </div>

      {/* ---------- ERROR ---------- */}
      {error && (
        <div className="text-sm text-rose-600">
          {error}
        </div>
      )}

      {/* ---------- CONTENT ---------- */}
      {tab === "users" && (
        <AdminUserTable
          users={users}
          onRoleChange={changeRole}
          onToggleActive={toggleActive}
          onRevoke={revoke}
        />
      )}

      {tab === "audit" && <AdminAudit />}
    </div>
  );
}

