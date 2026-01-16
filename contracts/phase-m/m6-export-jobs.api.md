# Phase M.6 — Export Job Lifecycle (API Contract)

## Purpose
Define the lifecycle and guarantees of async export jobs.

## Job Lifecycle
requested → running → completed | failed | cancelled

No other states allowed.

## Job Creation
Jobs are created ONLY from validated export requests (Phase M.1).
Direct job creation is forbidden.

## Job Schema (Conceptual)
{
  "id": "uuid",
  "export_request_id": "uuid",
  "status": "requested | running | completed | failed | cancelled",
  "progress": 0
}

