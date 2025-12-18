#!/usr/bin/env bash

# Omega-INFINITY Patch Auto-Repair v5
# Fault-tolerant version — NEVER stops on a single error
# Shows full debug logs and continues repairing all files.

# DO NOT USE: set -euo pipefail   # <-- too strict, stops script with no message

set -u   # only fail on undefined variable
IFS=$'\n\t'

PATCH_DIR="${1:-.graffi_helper_model/patches}"

echo "=== Omega-INFINITY Patch Auto-Repair v5 (Fault Tolerant) ==="
echo "Target directory: $PATCH_DIR"
echo

if [[ ! -d "$PATCH_DIR" ]]; then
  echo "ERROR: Patch directory missing: $PATCH_DIR"
  exit 1
fi

##############################
# Pad numbers without printf #
##############################
pad4() {
    local num="$1"
    num="${num##+(0)}"
    [[ -z "$num" ]] && num="0"

    case "${#num}" in
        1) echo "000$num" ;;
        2) echo "00$num"  ;;
        3) echo "0$num"   ;;
        *) echo "$num"    ;;
    esac
}

##############################
# Normalize Patch Filename   #
##############################
normalize_name() {
    local file="$1"
    local base=$(basename "$file")
    clean="${base// /_}"

    [[ "$clean" == *.patch ]] || clean="${clean}.patch"

    num_prefix=$(echo "$clean" | sed -n 's/^\([0-9]\+\).*/\1/p' || true)

    if [[ -z "$num_prefix" ]]; then
        rnd=$((9000 + RANDOM % 1000))
        echo "$(pad4 "$rnd")_${clean}"
        return
    fi

    rest="${clean#$num_prefix}"
    padded=$(pad4 "$num_prefix")
    echo "${padded}${rest}"
}

##############################
# Repair Single Patch File   #
##############################
repair_one() {
    local file="$1"
    local dir
    dir=$(dirname "$file")
    local base
    base=$(basename "$file")

    echo "--- Repairing: $base ---"

    # Normalize filename
    newname=$(normalize_name "$file")
    if [[ "$newname" != "$base" ]]; then
        echo "• Renaming: $base → $newname"
        mv "$file" "$dir/$newname" || echo "❌ Rename failed for $file"
        file="$dir/$newname"
        base="$newname"
    fi

    # temp working file
    tmp=$(mktemp /tmp/patchfix.XXXXXX)
    cp "$file" "$tmp" || echo "❌ Copy failed for $file"

    # Remove CRLF
    if grep -q $'\r' "$tmp" 2>/dev/null; then
        echo "• Removing CRLF..."
        tr -d '\r' < "$tmp" > "${tmp}.x" && mv "${tmp}.x" "$tmp"
    fi

    # Remove literal trailing $
    if grep -q '\$$' "$tmp" 2>/dev/null; then
        echo "• Removing trailing \$..."
        sed -i 's/\$$//' "$tmp" || true
    fi

    # Remove control characters
    echo "• Removing control chars..."
    awk '{ gsub(/[\x00-\x1F\x7F]/,""); print }' "$tmp" > "${tmp}.clean" \
        && mv "${tmp}.clean" "$tmp"

    # Ensure newline at EOF
    if [[ "$(tail -c1 "$tmp" | wc -l)" -eq 0 ]]; then
        echo >> "$tmp"
    fi

    # Ensure diff header exists
    if ! grep -q "^diff --git" "$tmp"; then
        echo "• Missing diff header — reconstructing..."
        guess=$(grep -E '^\+\+\+ ' "$tmp" | head -n1 | awk '{print $2}' || true)

        if [[ -n "$guess" ]]; then
            guess=$(echo "$guess" | sed 's@^a/@@; s@^b/@@; s@^/@@')
            {
                echo "diff --git a/$guess b/$guess"
                echo "--- a/$guess"
                echo "+++ b/$guess"
                cat "$tmp"
            } > "${tmp}.hdr"
            mv "${tmp}.hdr" "$tmp"
        else
            echo "❌ Could not reconstruct header for $file"
        fi
    fi

    # Fix malformed hunk headers
    if grep -q "^@@[^ ]" "$tmp"; then
        echo "• Fixing hunk headers..."
        sed -i 's/^@@\([^@]*\)@@/@@ \1 @@/' "$tmp" || true
    fi

    # Overwrite original
    mv "$tmp" "$file" || echo "❌ Failed to overwrite $file"

    echo "✔ Repaired: $file"
    echo
}

##############################
#          MAIN LOOP         #
##############################

count=0
for f in "$PATCH_DIR"/*.patch; do
    echo "Processing file: $f"
    repair_one "$f" || echo "❌ ERROR: Failed to repair $f (continuing...)"
    count=$((count + 1))
done

echo "=== COMPLETE: $count patches processed ==="
exit 0

