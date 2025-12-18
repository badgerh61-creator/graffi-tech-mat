#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-.graffi_helper_model/patches}"
mkdir -p "$OUT_DIR"
PATCH_FILE="$OUT_DIR/$(git rev-parse --short HEAD)_one_shot.patch"
git diff HEAD^..HEAD > "$PATCH_FILE"
if [ ! -s "$PATCH_FILE" ]; then
  echo "Empty patch. Nothing to save."
  rm -f "$PATCH_FILE"
  exit 2
fi

echo "Created: $PATCH_FILE"
if git apply --check "$PATCH_FILE" >/dev/null 2>&1; then
  echo "Patch validates with git apply --check"
else
  echo "Patch fails git apply --check. Inspect: $PATCH_FILE"
  exit 3
fi

exit 0

