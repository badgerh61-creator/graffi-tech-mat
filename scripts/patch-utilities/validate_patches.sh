#!/usr/bin/env bash
set -euo pipefail

# validate_patches.sh
# Usage: ./validate_patches.sh [patch_dir] [start_num] [end_num]
PATCH_DIR="${1:-.graffi_helper_model/patches}"
START="${2:-1}"
END="${3:-60}"

if [ ! -d "$PATCH_DIR" ]; then
  echo "ERROR: patch dir not found: $PATCH_DIR"
  exit 2
fi

WORKROOT=$(mktemp -d /tmp/graffival.XXXX)
cleanup() { rm -rf "$WORKROOT"; }
trap cleanup EXIT

summary_ok=0; summary_fail=0; summary_missing=0

for n in $(seq -f "%04g" "$START" "$END"); do
  # find the patch file matching prefix n_*
  f=$(ls "$PATCH_DIR"/${n}_*.patch 2>/dev/null | head -n1 || true)
  if [ -z "$f" ]; then
    echo "MISSING: ${n} — no file matching ${n}_*.patch"
    summary_missing=$((summary_missing+1))
    continue
  fi

  echo "---- Checking: $(basename "$f") ----"
  if [ ! -s "$f" ]; then
    echo "  FAIL: empty file"
    summary_fail=$((summary_fail+1))
    continue
  fi

  # prepare candidate file (dos2unix + ensure newline)
  cp "$f" "$WORKROOT/tmp.patch"
  if command -v dos2unix >/dev/null 2>&1; then
    dos2unix "$WORKROOT/tmp.patch" >/dev/null 2>&1 || true
  else
    tr -d '\r' < "$WORKROOT/tmp.patch" > "${WORKROOT}/tmp2.patch" && mv "${WORKROOT}/tmp2.patch" "$WORKROOT/tmp.patch" || true
  fi
  # ensure newline
  if [ -n "$(tail -c1 "$WORKROOT/tmp.patch")" ] && [ "$(tail -c1 "$WORKROOT/tmp.patch" | od -An -t u1 | tr -d ' ')" != "10" ]; then
    echo >> "$WORKROOT/tmp.patch"
  fi

  # create temporary worktree for check
  WT="$WORKROOT/wt_${n}"
  git worktree add --detach "$WT" >/dev/null 2>&1 || { echo "ERROR: git worktree failed (clean repo?)."; summary_fail=$((summary_fail+1)); continue; }
  pushd "$WT" >/dev/null

  if git apply --check "$WORKROOT/tmp.patch" >/tmp/graffival.out 2>&1; then
    echo "  OK: apply --check passed"
    summary_ok=$((summary_ok+1))
    sed -n '1,6p' /tmp/graffival.out || true
  else
    echo "  FAIL: apply --check failed"
    summary_fail=$((summary_fail+1))
    sed -n '1,80p' /tmp/graffival.out || true
  fi

  popd >/dev/null
  git worktree remove --force "$WT" >/dev/null 2>&1 || true
  echo
done

echo "SUMMARY: OK=${summary_ok} FAIL=${summary_fail} MISSING=${summary_missing}"
if [ "$summary_fail" -gt 0 ]; then
  exit 3
fi
exit 0

