import React from "react";

export default function AdminUserTable({
  users,
  onRoleChange,
  onToggleActive,
  onRevoke,
}) {
  return (
    <table className="w-full text-sm border">
      <thead className="bg-slate-100">
        <tr>
          <th className="p-2 text-left">Email</th>
          <th className="p-2">Role</th>
          <th className="p-2">Active</th>
          <th className="p-2">Actions</th>
        </tr>
      </thead>

      <tbody>
        {users.map((u) => (
          <tr key={u.id} className="border-t">
            <td className="p-2">{u.email}</td>

            <td className="p-2 text-center">
              <select
                value={u.role}
                onChange={(e) =>
                  onRoleChange(u.id, e.target.value)
                }
                className="border rounded px-1"
              >
                <option value="viewer">viewer</option>
                <option value="editor">editor</option>
                <option value="admin">admin</option>
              </select>
            </td>

            <td className="p-2 text-center">
              <input
                type="checkbox"
                checked={u.is_active}
                onChange={() =>
                  onToggleActive(u.id, !u.is_active)
                }
              />
            </td>

            <td className="p-2 text-center space-x-2">
              <button
                onClick={() => onRevoke(u.id)}
                className="text-xs text-rose-600 hover:underline"
              >
                Revoke Sessions
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

