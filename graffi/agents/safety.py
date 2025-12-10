# graffi/agents/safety.py
"""
Safety agent:
- Detects unsafe env secrets
- Checks CORS settings
- Scans repo for accidental secret leaks
"""

from pathlib import Path
import re

SUSPECT_VALUES = ["minioadmin", "change-me", "dev-secret", "password"]

def read_env(path: Path):
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out

def scan_repo_for_secrets(root: Path):
    findings = []
    pat = re.compile(r"(AKIA|AIza|SECRET|PRIVATE|PASSWORD|TOKEN|-----BEGIN)")
    for f in root.rglob("*.*"):
        if f.suffix in [".py", ".js", ".json", ".env", ".txt", ".yml"]:
            try:
                t = f.read_text(encoding="utf-8", errors="ignore")
                if pat.search(t[:4000]):
                    findings.append(str(f))
            except Exception:
                pass
    return findings

def analyze(root: str = "."):
    R = Path(root)
    out = {"env_issues": [], "cors": [], "secrets": []}

    for fname in [".env", ".env.template", ".env.prod", ".env.prod.template"]:
        p = R / fname
        if p.exists():
            env = read_env(p)
            for k, v in env.items():
                if v in SUSPECT_VALUES:
                    out["env_issues"].append({"file": fname, "key": k, "value": v})
                if k == "CORS_ORIGINS" and v.strip() in ["*", '["*"]']:
                    out["cors"].append({"file": fname, "value": v})
    out["secrets"] = scan_repo_for_secrets(R)
    return out

