#!/usr/bin/env bash
set -euo pipefail

# generate_patch_series.sh
# Usage: ./generate_patch_series.sh [out_dir] [branch-or-commit-range]
OUT_DIR="${1:-.graffi_helper_model/patches_from_commits}"
RANGE="${2:-HEAD}"

mkdir -p "$OUT_DIR"
echo "Generating patch series for: $RANGE -> $OUT_DIR"

i=1
# list commits in chronological order for the range (if range is single branch HEAD)
for c in $(git rev-list --reverse "$RANGE"); do
  parent=$(git rev-list --parents -n1 "$c" | awk '{print $2}')
  if [ -z "$parent" ]; then
    echo "Skipping root commit $c"
    continue
  fi
  msg=$(git log -1 --pretty=format:%s "$c" | tr ' ' '-' | tr -cd '[:alnum:]-_')
  name=$(printf "%04d_%s.patch" "$i" "$msg")
  git diff "$parent" "$c" > "$OUT_DIR/$name"
  if [ ! -s "$OUT_DIR/$name" ]; then
    rm -f "$OUT_DIR/$name"
  else
    echo "  • $name"
    i=$((i+1))
  fi
done

echo "Done. Generated $((i-1)) patches in $OUT_DIR"
exit 0

