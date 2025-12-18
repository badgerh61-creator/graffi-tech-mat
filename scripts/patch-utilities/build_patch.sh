#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-.graffi_helper_model/patches}"
mkdir -p "$OUT_DIR"
PATCH_FILE="$OUT_DIR/$(date +%Y%m%d%H%M%S)_last_commit.patch"
git diff HEAD^..HEAD > "$PATCH_FILE"
if [ ! -s "$PATCH_FILE" ]; then
  echo "No diff produced for HEAD^..HEAD"
  rm -f "$PATCH_FILE"
  exit 2
fi
echo "Patch created: $PATCH_FILE"
exit 0

