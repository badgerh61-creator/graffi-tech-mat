# Phase P — Observability & Metrics

## Purpose
Provide visibility into system behavior without altering outcomes.

---

## Signal Types

### Metrics
- Counters (monotonic)
- Histograms (latency)
- Gauges (current state)

### Events
- Structured, append-only
- Human-readable
- Correlated with trace_id

### Traces
- Spans around critical operations
- Parent/child relationships
- No payload data (metadata only)

---

## Observed Domains

- Geometry (K)
- Validation (L)
- Exports (M)
- Distribution (N)
- Automation (O)
- UI Command Flow (K-UI)

---

## Canonical Metrics (Initial)

### Geometry
- geometry.regeneration.count
- geometry.regeneration.duration_ms
- geometry.validation.failures.count

### Exports
- export.attempt.count
- export.success.count
- export.failure.count
- export.duration_ms

### Distribution
- distribution.request.count
- distribution.signed_url.created.count
- distribution.revocation.count

### Automation
- automation.job.run.count
- automation.job.retry.count
- automation.job.failure.count

---

## Trace Rules

- Every observed operation MAY start a span
- Spans MUST include trace_id
- No PII or geometry payloads in spans

---

## Exposure

- Metrics endpoint is read-only
- Metrics never require authentication (internal network)
- Events are not queryable via API (log-only)

---

## Forbidden

- Metrics used for authorization
- Metrics changing execution
- Hidden side effects
- Silent failures

