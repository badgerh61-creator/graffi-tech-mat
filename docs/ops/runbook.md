# Graffi-Tech-Mat Ops Runbook (H.8)

## Processes (Topology)
- API: FastAPI/Uvicorn service
- Worker: async job runner (jobs queue / automation)
- Scheduler: periodic triggers (Phase O jobs)
- Frontend: static build hosting (prod) / Vite dev server (dev)

## Health Endpoints
- GET /health  -> liveness (no DB)
- GET /ready   -> readiness (DB read-only check)

## Boot (Dev)
1) Start backend API
2) Start frontend dev server
3) Optional: start worker/scheduler

## Boot (Prod-like)
- API runs as one unit
- Worker runs separately
- Scheduler runs separately
- Frontend served as static build

## DB Upgrade
1) Run migrations (Phase H.6)
2) Restart API + workers

## Backup/Restore
See Phase H.7 procedures.
