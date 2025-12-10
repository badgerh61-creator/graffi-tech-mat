from pathlib import Path
def suggest_refactors(root=Path('.')):
    finds = []
    for p in root.rglob('*.py'):
        try:
            lines = p.read_text().splitlines()
            if len(lines) > 300:
                finds.append(str(p))
        except Exception:
            pass
    return {'candidates': finds}
