#!/bin/bash
set -e

PATCH_DIR="$1"

if [ ! -d "$PATCH_DIR" ]; then
  echo "Patch directory not found: $PATCH_DIR"
  exit 1
fi

echo "=== Importing patches as ordered commits ==="
echo "Patch dir: $PATCH_DIR"

# Create a new branch for patch import
BRANCH="patch-import/$(date +%Y%m%d%H%M%S)"
git branch "$BRANCH" >/dev/null 2>&1 || true
git checkout "$BRANCH"

# Get REAL patch list
PATCHES=($(ls -1 "$PATCH_DIR"/*.patch | sort))

echo "Found ${#PATCHES[@]} patches."

INDEX=1
for PATCH in "${PATCHES[@]}"; do
    NAME=$(basename "$PATCH")
    echo ""
    echo "→ [$INDEX/${#PATCHES[@]}] Importing: $NAME"

    if git apply --check "$PATCH"; then
        git apply "$PATCH"
        git add -A
        git commit -m "Apply patch: $NAME"
        echo "✔ Applied successfully"
    else
        echo "❌ FAILED to apply patch: $NAME"
        exit 1
    fi
    INDEX=$((INDEX+1))
done

echo ""
echo "=== COMPLETE: All patches imported correctly ==="
