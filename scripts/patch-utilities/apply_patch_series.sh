#!/usr/bin/env bash
set -euo pipefail

# apply_patch_series.sh
# Usage: ./apply_patch_series.sh [patch_dir] [--no-commit]
PATCH_DIR="${1:-.graffi_helper_model/patches}"
NO_COMMIT=false
if [ "${2:-}" == "--no-commit" ]; then NO_COMMIT=true; fi

if [ ! -d "$PATCH_DIR" ]; then
  echo "ERROR: patch dir not found: $PATCH_DIR"
  exit 2
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not a git repo"
  exit 3
fi

echo "Applying patch series from: $PATCH_DIR"
mapfile -t PATCHES < <(ls "$PATCH_DIR"/*.patch 2>/dev/null | sort -V)
if [ "${#PATCHES[@]}" -eq 0 ]; then
  echo "No patch files found"
  exit 0
fi

SAVEPOINT=$(git rev-parse --verify HEAD)
LOG=".graffi_helper_model/patches/apply.log"
mkdir -p "$(dirname "$LOG")"

for p in "${PATCHES[@]}"; do
  echo "-> $(basename "$p")"
  if git apply --check "$p" >/dev/null 2>&1; then
    git apply "$p"
    if [ "$NO_COMMIT" = false ]; then
      git add -A
      git commit -m "Apply patch: $(basename "$p")" >>"$LOG" 2>&1 || echo "Commit may have failed (no changes)"
      echo "  ✔ applied & committed"
    else
      echo "  ✔ applied (not committed)"
    fi
  else
    echo "  ✖ would not apply cleanly. Rolling back and aborting."
    git reset --hard "$SAVEPOINT"
    exit 4
  fi
done

echo "All patches applied."
exit 0

