# graffi/agents/evolution.py
"""
Evolution Agent:
- Tracks file hash changes
- Detects added/removed/modified Python files
- Integrates refactor agent suggestions
"""

from pathlib import Path
import hashlib
import json
from .refactor import suggest_refactors

def hash_file(path: Path):
    try:
        return hashlib.md5(path.read_bytes()).hexdigest()
    except Exception:
        return "0"

def analyze(root: str = "."):
    R = Path(root)
    snapshot_path = R / ".graffi_helper_model" / "snapshot.json"

    current = {}
    for f in R.rglob("*.py"):
        current[str(f)] = hash_file(f)

    old = {}
    if snapshot_path.exists():
        try:
            old = json.loads(snapshot_path.read_text()).get("files", {})
        except:
            old = {}

    drift = []
    for f, h in current.items():
        if f not in old:
            drift.append({"file": f, "change": "new"})
        elif old[f] != h:
            drift.append({"file": f, "change": "modified"})

    deleted = [f for f in old if f not in current]

    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps({"files": current}, indent=2))

    ref = suggest_refactors(root)

    return {
        "drift": drift,
        "deleted": deleted,
        "refactor_candidates": len(ref.get("suggested_snippets", [])),
    }

