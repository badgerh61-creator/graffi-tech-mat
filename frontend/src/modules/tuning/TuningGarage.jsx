import { useEffect, useState } from "react";
import { getAccessToken } from "../../utils/auth";

export default function TuningGarage({ snapshotId }) {
  const [tuning, setTuning] = useState(null);

  useEffect(() => {
    if (!snapshotId) return;

    const token = getAccessToken();

    fetch(`http://127.0.0.1:8000/snapshots/${snapshotId}/tuning`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then(setTuning)
      .catch(console.error);
  }, [snapshotId]);

  if (!tuning) return <div>Loading tuning state...</div>;

  return (
    <div>
      <h2>Tuning Garage (Read-Only)</h2>

      <section>
        <h3>Engine</h3>
        <pre>{JSON.stringify(tuning.engine, null, 2)}</pre>
      </section>

      <section>
        <h3>Suspension</h3>
        <pre>{JSON.stringify(tuning.suspension, null, 2)}</pre>
      </section>

      <section>
        <h3>Wheels</h3>
        <pre>{JSON.stringify(tuning.wheels, null, 2)}</pre>
      </section>

      <section>
        <h3>Metrics</h3>
        <pre>{JSON.stringify(tuning.metrics, null, 2)}</pre>
      </section>
    </div>
  );
}

