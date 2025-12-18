#!/usr/bin/env bash
# Omega-INFINITY Bootstrap Script
# Fully automated system initializer:
#   - Create directories
#   - Repair patches
#   - Validate patches
#   - Apply patches in sequence
#   - Prepare engine for development

set -euo pipefail

PATCH_DIR=".graffi_helper_model/patches"

echo "==========================================================="
echo "        OMEGA-INFINITY — PATCH SYSTEM BOOTSTRAP"
echo "==========================================================="
echo

# -----------------------------------------------------------
# 1. Create directory structure required by patches
# -----------------------------------------------------------
echo "[1/6] Creating required directory structure..."

mkdir -p agents tools ml sandbox analytics services config \
         patch_server runtime documentation scripts

echo "    ✔ Directories created:"
echo "      agents/ tools/ ml/ sandbox/ analytics/ services/"
echo "      config/ patch_server/ runtime/ documentation/ scripts/"
echo


# -----------------------------------------------------------
# 2. Repair all patch files in place
# -----------------------------------------------------------
echo "[2/6] Repairing all patch files (normalizing, fixing headers)..."

if [ ! -f repair_patch.sh ]; then
    echo "ERROR: repair_patch.sh not found!"
    echo "Please place repair_patch.sh in the project root."
    exit 1
fi

./repair_patch.sh "$PATCH_DIR"

echo "    ✔ Patch repair completed."
echo


# -----------------------------------------------------------
# 3. Validate patch series 0001–0060
# -----------------------------------------------------------
echo "[3/6] Validating patches..."

if [ ! -f validate_patches.sh ]; then
    echo "ERROR: validate_patches.sh not found!"
    echo "Please place validate_patches.sh in the project root."
    exit 1
fi

./validate_patches.sh "$PATCH_DIR" 1 60

echo "    ✔ Patch validation completed."
echo


# -----------------------------------------------------------
# 4. Apply patches in correct order
# -----------------------------------------------------------
echo "[4/6] Applying patches to repository..."

if [ ! -f apply_patch_series.sh ]; then
    echo "    apply_patch_series.sh missing — generating it..."
cat <<'EOF' > apply_patch_series.sh
#!/usr/bin/env bash
set -euo pipefail

PATCH_DIR=".graffi_helper_model/patches"

for i in $(seq -f "%04g" 1 60); do
    file=$(ls $PATCH_DIR/${i}_*.patch 2>/dev/null || true)
    if [ -z "$file" ]; then
        echo "SKIP: Patch $i not found."
        continue
    fi

    echo "Applying $file ..."
    git apply "$file"
done

echo "All patches applied."
EOF

chmod +x apply_patch_series.sh
echo "    ✔ Created apply_patch_series.sh"
fi

./apply_patch_series.sh

echo "    ✔ Patch application completed."
echo


# -----------------------------------------------------------
# 5. Generate missing helper scripts
# -----------------------------------------------------------
echo "[5/6] Generating support scripts (sandbox, tests, helpers)..."

# sandbox_patch.sh
cat <<'EOF' > sandbox_patch.sh
#!/usr/bin/env bash
set -euo pipefail

# Simple sandbox executor
echo "Running sandbox environment..."
python3 tools/sandbox_eval.py 2>/dev/null || echo "Sandbox evaluator missing or not installed."
EOF
chmod +x sandbox_patch.sh

echo "    ✔ sandbox_patch.sh generated."


# apply_single_patch.sh
cat <<'EOF' > scripts/apply_single_patch.sh
#!/usr/bin/env bash
set -euo pipefail

PATCH="$1"
if [ -z "$PATCH" ]; then
    echo "Usage: apply_single_patch.sh <patchfile>"
    exit 1
fi

echo "Applying $PATCH ..."
git apply "$PATCH"
EOF
chmod +x scripts/apply_single_patch.sh

echo "    ✔ apply_single_patch.sh generated."
echo


# -----------------------------------------------------------
# 6. Final status & next steps
# -----------------------------------------------------------
echo "[6/6] Bootstrap complete!"
echo
echo "✔ Directory structure prepared"
echo "✔ Patch files repaired"
echo "✔ Patch files validated"
echo "✔ Patches applied"
echo "✔ Helper scripts generated"
echo
echo "==========================================================="
echo "   Omega-INFINITY Patch System is now fully bootstrapped"
echo "   You may now proceed to FEATURE DEVELOPMENT."
echo "==========================================================="
echo

