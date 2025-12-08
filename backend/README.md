# Graffi Backend (Standard Production)

This backend scaffold provides:
- FastAPI app
- PostgreSQL-ready SQLAlchemy models
- MinIO / S3 storage integration (boto3)
- Redis + RQ worker for background tasks (thumbnails)
- Presigned upload support
- Asset / Model / Preset endpoints
- Dockerfile for container builds

## Quick start (Docker Compose recommended)
Create a docker-compose.yml at the project root (example provided in project docs), then run:

```bash
docker compose up --build
```

API docs: http://localhost:8000/docs
MinIO console: http://localhost:9001 (minioadmin/minioadmin)
