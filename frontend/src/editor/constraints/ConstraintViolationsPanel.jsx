export default function ConstraintViolationsPanel({ violations }) {
  if (!violations?.length) return null;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold text-red-700">
        Constraint Violations
      </div>
      <div className="space-y-2">
        {violations.map((v, i) => (
          <div key={v.constraint_id || i} className="border rounded p-2">
            <div className="text-sm font-semibold">{v.kind}</div>
            <div className="text-xs opacity-80">{v.message}</div>
            {v.data ? (
              <pre className="text-[11px] opacity-75 overflow-auto mt-1">
{JSON.stringify(v.data, null, 2)}
              </pre>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}
