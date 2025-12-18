#!/usr/bin/env bash
set -euo pipefail

TMPDIR="$(mktemp -d /tmp/graffipreview.XXXX)"
PATCH_DIR="$TMPDIR/patches"
mkdir -p "$PATCH_DIR"
echo "=== PREVIEW: Auto-Rebuilder Dry Run ==="
echo "Temp: $TMPDIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not inside a git repo"
  exit 1
fi

i=1
for c in $(git rev-list --reverse HEAD); do
  parent=$(git rev-list --parents -n1 "$c" | awk '{print $2}')
  if [ -z "$parent" ]; then continue; fi
  msg=$(git log -1 --pretty=format:%s "$c" | tr ' ' '-' | tr -cd '[:alnum:]-_')
  name=$(printf "%04d_%s.patch" "$i" "$msg")
  git diff "$parent" "$c" > "$PATCH_DIR/$name"
  if [ ! -s "$PATCH_DIR/$name" ]; then rm -f "$PATCH_DIR/$name"; else i=$((i+1)); fi
done

if [ -z "$(ls -A "$PATCH_DIR")" ]; then
  echo "No patches created. Exiting."
  rm -rf "$TMPDIR"
  exit 0
fi

FAILED=0
for p in "$PATCH_DIR"/*.patch; do
  echo "Checking: $(basename "$p")"
  if git apply --check "$p" >/tmp/graffipreview.out 2>&1; then
    echo "  ✔ would apply cleanly"
  else
    echo "  ✖ would NOT apply cleanly"
    sed -n '1,40p' /tmp/graffipreview.out || true
    FAILED=$((FAILED+1))
  fi
done

echo "Summary: total=$(ls -1 "$PATCH_DIR" | wc -l) failed=$FAILED"
echo "Temp preserved at: $TMPDIR"
exit $([ "$FAILED" -gt 0 ] && echo 3 || echo 0)

