export function ImageExportButton({ snapshot }) {
  if (snapshot.status !== "completed") return null;

  return <button>Export Image</button>;
}

