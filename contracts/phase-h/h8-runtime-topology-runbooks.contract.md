### `contracts/phase-h/h8-runtime-topology-runbooks.contract.md`

```md
# Phase H.8 — Runtime Topology + Health/Ready + Ops Runbooks (Ops-Grade)

## Purpose (LOCKED)
Make the system operationally runnable and observable as separate runtime units:
- API
- Worker(s)
- Scheduler
- Frontend

Add health/readiness endpoints and provide runbooks without changing kernel behavior.

## Scope
- Add /health (liveness) and /ready (readiness) endpoints
- Add DB readiness check (read-only)
- Add ops runbook documentation
- Add reference docker-compose topology (non-authoritative, optional)
- Add tests proving endpoints work and readiness fails safely when DB is unavailable

## Non-Negotiable Invariants
1) Additive only: no removal/renaming of existing functions/models/routes.
2) /health MUST NOT touch DB (always fast).
3) /ready MAY check DB but MUST be read-only and bounded.
4) No changes to snapshot/tool/kernel behavior.
5) Must be safe on sqlite/local dev.

## Endpoints
GET /health
- 200 always
- returns {"status":"ok","service":"api","version":...optional}

GET /ready
- 200 only if dependencies are ready (DB check at minimum)
- 503 if DB not reachable
- returns {"ready":true/false,"checks":{...}}

## Tests
- /health returns 200 and does not require auth
- /ready returns 200 when DB is reachable
- /ready returns 503 when DB check fails (monkeypatched)
```

---

