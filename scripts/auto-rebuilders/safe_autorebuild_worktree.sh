#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not in a git repository."
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
TMPROOT="$(mktemp -d /tmp/graffirebuild.XXXX)"
PATCH_DIR="$TMPROOT/patches"
WT_DIR="$TMPROOT/worktree"
mkdir -p "$PATCH_DIR" "$WT_DIR"

echo "=== SAFE AUTO-REBUILDER (worktree) ==="
echo "Temporary root: $TMPROOT"

# generate patch series from commits (one patch per commit)
i=1
for c in $(git rev-list --reverse HEAD); do
  parent=$(git rev-list --parents -n1 "$c" | awk '{print $2}')
  if [ -z "$parent" ]; then
    continue
  fi
  msg=$(git log -1 --pretty=format:%s "$c" | tr ' ' '-' | tr -cd '[:alnum:]-_')
  name=$(printf "%04d_%s.patch" "$i" "$msg")
  git diff "$parent" "$c" > "$PATCH_DIR/$name"
  if [ ! -s "$PATCH_DIR/$name" ]; then
    rm -f "$PATCH_DIR/$name"
  else
    i=$((i+1))
  fi
done

if [ -z "$(ls -A "$PATCH_DIR")" ]; then
  echo "No patches created from commits. Exiting."
  rm -rf "$TMPROOT"
  exit 0
fi

echo "Adding detached worktree ..."
git worktree add --detach "$WT_DIR" HEAD >/dev/null 2>&1 || { echo "Failed to create worktree"; rm -rf "$TMPROOT"; exit 1; }

pushd "$WT_DIR" >/dev/null

APPLY_FAIL=0
for p in "$PATCH_DIR"/*.patch; do
  echo "Applying: $(basename "$p")"
  if git apply --check "$p" >/tmp/graffireapply.err 2>&1; then
    if ! git apply "$p" >>"$TMPROOT/apply.log" 2>&1; then
      echo "Failed to apply $p (logged)"
      APPLY_FAIL=1
      break
    fi
  else
    echo "Would NOT apply: $(sed -n '1,60p' /tmp/graffireapply.err || true)"
    APPLY_FAIL=1
    break
  fi
done

# run simple build/test if all applied
BUILD_ERRORS=0
if [ "$APPLY_FAIL" -eq 0 ]; then
  if [ -f "requirements.txt" ]; then
    if command -v pip >/dev/null 2>&1; then
      pip install -r requirements.txt >>"$TMPROOT/build.log" 2>&1 || BUILD_ERRORS=$((BUILD_ERRORS+1))
    fi
  fi
  if command -v pytest >/dev/null 2>&1; then
    pytest -q >>"$TMPROOT/build.log" 2>&1 || BUILD_ERRORS=$((BUILD_ERRORS+1))
  fi
fi

popd >/dev/null

if [ "$APPLY_FAIL" -ne 0 ]; then
  echo "APPLY FAILURE. Worktree preserved at: $WT_DIR"
  echo "To remove: git worktree remove --force '$WT_DIR' && rm -rf '$TMPROOT'"
  exit 2
fi
if [ "$BUILD_ERRORS" -ne 0 ]; then
  echo "BUILD/TESTS reported issues. Worktree preserved at: $WT_DIR"
  exit 3
fi

echo "SUCCESS. Worktree at: $WT_DIR"
echo "Temp root: $TMPROOT"
exit 0

