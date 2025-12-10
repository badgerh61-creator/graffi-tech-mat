# graffi/agents/infra.py
"""
Infra agent:
- Validates docker-compose for missing healthchecks, restart policies, duplicate ports, bad volumes.
"""

from pathlib import Path
import yaml
from collections import defaultdict

def _load_compose(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        return {"__load_error__": str(e)}

def analyze(root: str = "."):
    R = Path(root)
    out = {"compose_files": {}, "warnings": []}

    for f in ["docker-compose.yml", "docker-compose.prod.yml", "docker-compose.override.yml"]:
        p = R / f
        if not p.exists():
            continue

        cfg = _load_compose(p)
        out["compose_files"][f] = {"services": []}

        if "__load_error__" in cfg:
            out["compose_files"][f]["error"] = cfg["__load_error__"]
            continue

        svc = cfg.get("services", {})
        ports = defaultdict(list)

        for name, spec in svc.items():
            info = {"name": name}

            if "healthcheck" not in spec:
                out["warnings"].append(f"{f}:{name} missing healthcheck")

            if "restart" not in spec:
                out["warnings"].append(f"{f}:{name} missing restart policy")

            for pdef in spec.get("ports", []) or []:
                if isinstance(pdef, str) and ":" in pdef:
                    hp = pdef.split(":")[0]
                    ports[hp].append(f"{f}:{name}")

            for vol in spec.get("volumes", []) or []:
                if isinstance(vol, str) and ":" in vol:
                    host = vol.split(":")[0]
                    if host.startswith("./"):
                        if not (R / host).exists():
                            out["warnings"].append(f"{f}:{name} missing host volume path: {host}")

            out["compose_files"][f]["services"].append(info)

        for p, svc_list in ports.items():
            if len(svc_list) > 1:
                out["warnings"].append(f"Port {p} duplicated in {svc_list}")

    return out

