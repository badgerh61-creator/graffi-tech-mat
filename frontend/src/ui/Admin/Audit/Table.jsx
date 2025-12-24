import React from "react";

export default function AdminAuditTable({ logs }) {
  // 🛡️ Small guard — empty / initial state
  if (!logs || logs.length === 0) {
    return (
      <div className="text-sm text-slate-500">
        No audit events found.
      </div>
    );
  }

  return (
    <table className="w-full text-sm border">
      <thead className="bg-slate-100">
        <tr>
          <th className="p-2 text-left">Time</th>
          <th className="p-2">User</th>
          <th className="p-2">Action</th>
          <th className="p-2">Resource</th>
          <th className="p-2">Details</th>
        </tr>
      </thead>

      <tbody>
        {logs.map((l) => (
          <tr key={l.id} className="border-t align-top">
            <td className="p-2 whitespace-nowrap">
              {new Date(l.created_at).toLocaleString()}
            </td>

            <td className="p-2 text-center">
              {l.user_id ?? "system"}
            </td>

            <td className="p-2 text-center font-mono">
              {l.action}
            </td>

            <td className="p-2 text-center">
              {l.resource_type}
              {l.resource_id && ` #${l.resource_id}`}
            </td>

            <td className="p-2 text-xs text-slate-600">
              {l.extra ? (
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(l.extra, null, 2)}
                </pre>
              ) : (
                "-"
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

