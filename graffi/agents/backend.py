# graffi/agents/backend.py
"""
Backend agent:
- Checks Alembic env.py imports
- Detects missing __init__.py in backend/app/*
- Checks requirements.txt for FastAPI deps
"""

from pathlib import Path
import re

REQUIRED_PKGS = ["db", "api", "services", "worker", "core", "models"]

def find_missing_inits(root):
    R = Path(root) / "backend" / "app"
    missing = []
    if not R.exists():
        return missing
    for pkg in REQUIRED_PKGS:
        p = R / pkg
        if p.exists() and not (p / "__init__.py").exists():
            missing.append(str(p))
    return missing

def check_alembic_env(root):
    env = Path(root) / "alembic" / "env.py"
    if not env.exists():
        return {"present": False}
    txt = env.read_text(encoding="utf-8", errors="ignore")
    return {
        "present": True,
        "has_target_metadata": ("target_metadata" in txt)
    }

def check_requirements(root):
    req = Path(root) / "backend" / "requirements.txt"
    out = {"present": req.exists(), "missing": []}
    if not req.exists():
        return out

    txt = req.read_text(encoding="utf-8")
    expected = ["email-validator", "uvicorn", "fastapi", "alembic"]
    for pkg in expected:
        if pkg not in txt:
            out["missing"].append(pkg)
    return out

def analyze(root: str = "."):
    return {
        "missing_inits": find_missing_inits(root),
        "alembic_checks": check_alembic_env(root),
        "requirements": check_requirements(root),
    }

