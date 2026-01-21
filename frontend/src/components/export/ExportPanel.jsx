export default function ExportPanel({ snapshots }) {
  const hasDraft = snapshots.some(
    (s) => s.status === "draft"
  );

  const exportDisabled = hasDraft;

  return (
    <div>
      <button disabled={exportDisabled}>
        Export
      </button>

      {exportDisabled && (
        <p style={{ color: "#b58900", fontSize: 12 }}>
          Finalize draft before exporting
        </p>
      )}
    </div>
  );
}

