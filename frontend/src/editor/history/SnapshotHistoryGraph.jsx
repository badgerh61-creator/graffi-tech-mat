export default function SnapshotHistoryGraph({
  history,
  activeSnapshotId,
  onNavigate,
}) {
  if (!history.length) return null;

  return (
    <div data-testid="history-graph">
      {history.map((s) => (
        <div
          key={s.id}
          data-testid={`snapshot-${s.id}`}
          className={s.id === activeSnapshotId ? "active" : ""}
          onClick={() => onNavigate?.(s.id)}
        >
          {s.id}
        </div>
      ))}

      <button onClick={() => onNavigate(history.at(-2)?.id)}>
        Undo
      </button>
    </div>
  );
}

