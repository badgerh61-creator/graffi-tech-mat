#!/bin/sh
set -e
mc=/usr/bin/mc
sleep 3
$mc alias set local http://minio:9000 minioadmin minioadmin
$mc mb -p local/graffi-assets || true
$mc anonymous set download local/graffi-assets/thumbnails || true
echo "MinIO initialized."
