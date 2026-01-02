import { useEffect, useState } from "react";
import type { Job } from "../../types/job.types";
import { fetchJobs } from "../../services/jobService";

export default function JobPanel() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    setLoading(true);

    fetchJobs()
      .then((items) => {
        if (!alive) return;
        setJobs(items);
      })
      .catch((err) => {
        if (!alive) return;
        setError(
          err?.message ?? "Failed to load jobs"
        );
      })
      .finally(() => {
        if (!alive) return;
        setLoading(false);
      });

    return () => {
      alive = false;
    };
  }, []);

  return (
    <div className="job-panel">
      <h3>Background Jobs</h3>

      {loading && <p>Loading jobs…</p>}

      {!loading && error && (
        <p className="panel-error">{error}</p>
      )}

      {!loading && !error && jobs.length === 0 && (
        <p className="panel-empty">
          No background jobs.
        </p>
      )}

      {jobs.map((job) => (
        <div key={job.id} className="job-row">
          <div className="job-header">
            <strong>{job.type}</strong>
            <span>{job.status}</span>
          </div>

          <progress
            value={job.progress}
            max={100}
          />

          {job.status === "failed" && (
            <p className="job-error">
              {job.error}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}

