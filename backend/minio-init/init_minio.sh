#!/bin/sh
set -e

echo "⏳ Waiting for MinIO to become ready..."
sleep 8

mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

# Create bucket (ignore error if exists)
mc mb -p local/graffi-assets || true

# Make bucket public
mc anonymous set public local/graffi-assets || true

echo "✅ MinIO bucket 'graffi-assets' initialized."
