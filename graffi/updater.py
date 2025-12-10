from pathlib import Path
import json, time, difflib, shutil
from .semantic import build_semantic_model
from .core import ensure_dir, backup, write_json, MODEL_DIR

CANDIDATE_NAME = "candidate_helper.py"
HISTORY_FILE = MODEL_DIR / "history.json"
PATCH_DIR = MODEL_DIR / "patches"

def log_history(event: str, data: dict = None):
    ensure_dir(MODEL_DIR)
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text())
        except:
            history = []
    record = {"time": time.asctime(), "event": event, "data": data or {}}
    history.append(record)
    HISTORY_FILE.write_text(json.dumps(history, indent=2))

def regenerate_modules():
    model = build_semantic_model(Path('.'))
    out_dir = MODEL_DIR / "generated"
    ensure_dir(out_dir)
    (out_dir / "semantic.py").write_text(f'"""Auto-regenerated semantic module: {time.asctime()}"""\n') 
    (out_dir / "docs.py").write_text('# regenerated docs\n')
    (out_dir / "conflicts.py").write_text('# regenerated conflicts\n')
    log_history('regenerate_modules', {'generated_dir': str(out_dir)})
    return out_dir

def generate_patch(original: Path, updated: Path):
    ensure_dir(PATCH_DIR)
    orig_text = original.read_text().splitlines() if original.exists() else []
    new_text = updated.read_text().splitlines() if updated.exists() else []
    diff = difflib.unified_diff(orig_text, new_text, fromfile=str(original), tofile=str(updated), lineterm="")
    patch_path = PATCH_DIR / f"{original.name}.patch"
    patch_path.write_text("\n".join(diff))
    log_history('patch_generated', {'patch': str(patch_path)})
    return patch_path

def analyze_evolution():
    model = build_semantic_model(Path('.'))
    suggestions = {'missing_handlers':[], 'missing_imports':[], 'recommended_commands':[]}
    for file, info in model.get('python', {}).items():
        if file.endswith('router.py') and not info.get('functions'):
            suggestions['missing_handlers'].append(file)
        if 'fastapi' not in "".join(info.get('imports', [])):
            suggestions['missing_imports'].append(file)
    evo_file = MODEL_DIR / 'evolution_suggestions.json'
    write_json(evo_file, suggestions)
    log_history('evolution_analysis', suggestions)
    return evo_file

def generate_candidate():
    ensure_dir(MODEL_DIR)
    model = build_semantic_model(Path('.'))
    candidate_path = MODEL_DIR / CANDIDATE_NAME
    candidate_code = f"""# Candidate helper generated: {time.asctime()}\nprint('candidate generated')\n"""
    candidate_path.write_text(candidate_code)
    log_history('candidate_generated', {'candidate_file': str(candidate_path)})
    return candidate_path

def apply_candidate(target: Path = Path('graffi_helper.py')):
    candidate_path = MODEL_DIR / CANDIDATE_NAME
    if not candidate_path.exists():
        raise FileNotFoundError('No candidate helper found.')
    backup(target)
    target.write_text(candidate_path.read_text())
    log_history('candidate_applied', {'applied_to': str(target)})
    return target
