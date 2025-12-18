#!/usr/bin/env bash
set -euo pipefail

# validate_foundation.sh
# High-level validation:
#   1. Validates synthetic patches 0001–0060
#   2. (Optional) Runs sandbox test
#   3. (Optional) Runs ML/analytics tests
#   4. (Optional) Runs autonomy agent

PATCH_DIR=".graffi_helper_model/patches"
PSTART=1
PEND=60

echo "=== Omega-INFINITY Foundation Validation ==="
echo "Checking patches ${PSTART}–${PEND}"
echo

# 1. Ensure patch folder exists
if [ ! -d "$PATCH_DIR" ]; then
  echo "ERROR: Patch directory not found: $PATCH_DIR"
  exit 2
fi

# 2. Patch validation
echo "→ Running patch validator..."
./scripts/validate_patches.sh "$PATCH_DIR" "$PSTART" "$PEND" || {
  echo "❌ Patch validation failed. Fix patches before continuing."
  exit 3
}
echo "✔ Patch validator completed OK"
echo

# 3. Sandbox test (optional)
echo "→ Running sandbox test (optional)"
if [ -f "./tools/sandbox_eval.py" ]; then
  python3 ./tools/sandbox_eval.py || { echo "❌ Sandbox test failed"; exit 4; }
  echo "✔ Sandbox test passed"
else
  echo "No sandbox evaluator found → skipping"
fi
echo

# 4. Analytics/ML pipeline tests (optional)
echo "→ Running ML/Analytics checks (optional)"

if [ -f "./analytics/pipeline.py" ]; then
  python3 ./analytics/pipeline.py || echo "pipeline failed"
else
  echo "analytics/pipeline.py missing"
fi

if [ -f "./ml/trainer.py" ]; then
  python3 ./ml/trainer.py || echo "trainer failed"
else
  echo "ml/trainer.py missing"
fi

if [ -f "./ml/inference.py" ]; then
  python3 ./ml/inference.py || echo "inference failed"
else
  echo "ml/inference.py missing"
fi

echo "✔ ML/Analytics placeholders executed"
echo

# 5. Autonomy controller (optional)
echo "→ Running autonomy controller (optional)"
if [ -f "./agents/autonomy_controller.py" ]; then
  python3 ./agents/autonomy_controller.py || { echo "❌ Autonomy controller failed"; exit 5; }
  echo "✔ Autonomy controller OK"
else
  echo "No autonomy controller found → skipping"
fi
echo

echo "=== Foundation validation complete ==="
echo "If everything passed, you may start building product features."

