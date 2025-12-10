# graffi/agents/frontend.py
"""
Frontend agent:
- Checks admin build existence
- Reads package.json
- Scans for fetch/axios backend calls
"""

from pathlib import Path
import json
import re

def analyze(root: str = "."):
    R = Path(root)
    out = {"admin_build": False, "package_scripts": {}, "api_calls_found": [], "notes": []}

    admin_dist = R / "frontend" / "admin" / "dist"
    if admin_dist.exists() and any(admin_dist.rglob("*")):
        out["admin_build"] = True
    else:
        out["notes"].append("frontend/admin/dist missing")

    pkg = R / "frontend" / "package.json"
    if pkg.exists():
        try:
            pj = json.loads(pkg.read_text(encoding="utf-8"))
            out["package_scripts"] = pj.get("scripts", {})
        except Exception as e:
            out["notes"].append(f"Cannot parse package.json: {e}")

    pattern = re.compile(r"(fetch\(|axios\.(get|post|put|delete))")
    for p in R.rglob("*.js"):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
            if pattern.search(t):
                out["api_calls_found"].append(str(p.relative_to(R)))
        except Exception:
            continue

    return out

