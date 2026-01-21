import { getAccessToken } from "../../utils/auth";

export default function FinalizeDraftButton({ snapshot, onFinalized }) {
  if (!snapshot || snapshot.status !== "draft") return null;

  const finalize = async () => {
    if (!confirm("Finalize this draft? Editing will lock.")) return;

    const token = getAccessToken();

    const res = await fetch(
      `http://127.0.0.1:8000/snapshots/${snapshot.id}/finalize`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!res.ok) {
      alert("Finalize failed");
      return;
    }

    onFinalized();
  };

  return (
    <button onClick={finalize}>
      Finalize Design
    </button>
  );
}

