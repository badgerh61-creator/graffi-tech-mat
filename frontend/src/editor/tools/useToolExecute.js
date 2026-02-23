import { getAccessToken } from "../../utils/auth";

export function useToolExecute() {
  async function execute({ snapshotId, station, tool, payload }) {
    const token = getAccessToken();

    const res = await fetch("http://127.0.0.1:8000/tools/execute", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        snapshot_id: snapshotId,
        station,
        tool,
        payload,
      }),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Tool execute failed: ${res.status} ${text}`);
    }

    return res.json();
  }

  return { execute };
}
