from pathlib import Path
import shutil, subprocess, time, json, os
from typing import List, Optional

ROOT = Path.cwd()
BACKUP_DIR = ROOT / '.graffi_helper_backups'
MODEL_DIR = ROOT / '.graffi_helper_model'

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def backup(p: Path) -> Optional[Path]:
    ensure_dir(BACKUP_DIR)
    if not p.exists():
        return None
    ts = int(time.time())
    target = BACKUP_DIR / f"{p.name}.backup.{ts}"
    if p.is_dir():
        shutil.copytree(p, target)
    else:
        shutil.copy2(p, target)
    return target

def run(cmd: List[str], cwd: Path = None, capture_output=False):
    print(f"$ {' '.join(cmd)}")
    try:
        return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=capture_output, text=True)
    except FileNotFoundError:
        print(f"Tool not found: {cmd[0]}")
        return None

def write_json(p: Path, data):
    ensure_dir(p.parent)
    p.write_text(json.dumps(data, indent=2))
