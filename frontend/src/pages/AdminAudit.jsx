import React, { useEffect, useState } from "react";
import { auditApi } from "../api/audit";
import { normalizeApiError } from "../api/errors";
import AdminAuditTable from "../ui/Admin/Audit/Table";

export default function AdminAudit() {
  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState(1);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);
    setError(null);

    try {
      const res = await auditApi.list({ page, limit: 200 });
      setLogs(res.data.items);
    } catch (err) {
      setError(normalizeApiError(err));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [page]);

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">Audit Log</h1>

      {error && (
        <div className="text-sm text-rose-600">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-sm text-slate-500">
          Loading…
        </div>
      ) : (
        <AdminAuditTable logs={logs} />
      )}

      <div className="flex gap-2">
        <button
          className="btn-sm"
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
        >
          Prev
        </button>
        <button
          className="btn-sm"
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}

