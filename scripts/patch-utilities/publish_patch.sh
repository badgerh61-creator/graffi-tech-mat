#!/usr/bin/env bash
set -euo pipefail

# publish_patch.sh
# Uploads a patch to the Signing Server
# Usage:
#   ./scripts/patch-utilities/publish_patch.sh /path/to/patch.patch http://127.0.0.1:8000 API_KEY_VALUE

PATCH_FILE="${1:-}"
SERVER_URL="${2:-}"
API_KEY="${3:-}"

echo "=== Signing Server Patch Publisher ==="

# --- Validate parameters ---
if [[ -z "$PATCH_FILE" || -z "$SERVER_URL" || -z "$API_KEY" ]]; then
    echo "Usage: $0 <patch_file> <signing_server_url> <api_key>"
    exit 1
fi

if [[ ! -f "$PATCH_FILE" ]]; then
    echo "❌ ERROR: Patch file not found: $PATCH_FILE"
    exit 1
fi

echo "✔ Patch file: $PATCH_FILE"
echo "✔ Server: $SERVER_URL"

# --- Validate patch formatting ---
echo "Checking patch formatting..."
if git apply --check "$PATCH_FILE" 2>/tmp/publish_patch_check.log; then
    echo "✔ Patch is valid"
else
    echo "❌ Patch failed validation:"
    sed -n '1,80p' /tmp/publish_patch_check.log
    exit 1
fi

# --- Publish to server ---
echo "Uploading patch to signing server..."

HTTP_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" \
    -X POST "$SERVER_URL/api/patch/upload" \
    -H "Authorization: Bearer ${API_KEY}" \
    -F "file=@${PATCH_FILE}"
)

# extract body + status
HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed -e 's/HTTPSTATUS\:.*//g')
HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

# --- Interpret response ---
if [[ "$HTTP_STATUS" -eq 200 || "$HTTP_STATUS" -eq 201 ]]; then
    echo "✔ Patch uploaded successfully!"
    echo "$HTTP_BODY"
else
    echo "❌ Upload failed with status $HTTP_STATUS"
    echo "$HTTP_BODY"
    exit 1
fi

echo "=== DONE ==="

