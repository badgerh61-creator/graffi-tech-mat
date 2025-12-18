#!/usr/bin/env bash
set -euo pipefail

PATCH_DIR="${1:-.graffi_helper_model/patches}"
echo "=== AUTO-REBUILDER (hybrid import + validate) ==="

./scripts/repair_patch.sh "$PATCH_DIR"
./scripts/import_patches_as_commits.sh "$PATCH_DIR"

echo "Imported patches into a new branch. Run generate_patch_series.sh if you want canonical commit-based patches."
echo "Now running validation on the original patch set (best-effort)..."
./scripts/validate_patches.sh "$PATCH_DIR" 1 60 || {
  echo "Some original static patches did not validate; inspect outputs and fix before proceeding."
  exit 3
}

echo "Previewing rebuild..."
./scripts/preview_autorebuild.sh || echo "Preview reported issues."

echo "Done."
exit 0

