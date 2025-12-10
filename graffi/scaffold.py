from pathlib import Path
from .core import backup
REQUIRED_STUBS = {
    'frontend': ['src/engine/SceneCanvas.jsx','src/store/materialStore.js'],
    'backend': ['app/main.py','app/api/__init__.py']
}

def scaffold_validate(root=Path('.'), fix=False):
    issues = {'missing':[], 'fixed':[]}
    base = Path(root)
    if (base/'frontend').exists():
        for rel in REQUIRED_STUBS['frontend']:
            p = base/'frontend'/rel
            if not p.exists():
                issues['missing'].append(str(p))
                if fix:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text('// auto-generated stub\nexport default {}\n')
                    issues['fixed'].append(str(p))
    else:
        issues['missing'].append('frontend/ not found')
    if (base/'backend').exists():
        for rel in REQUIRED_STUBS['backend']:
            p = base/'backend'/rel
            if not p.exists():
                issues['missing'].append(str(p))
                if fix:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    if p.name.endswith('.py'):
                        p.write_text('from fastapi import FastAPI\napp = FastAPI()\n')
                    issues['fixed'].append(str(p))
    else:
        issues['missing'].append('backend/ not found')
    return issues
