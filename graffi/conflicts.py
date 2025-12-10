from pathlib import Path
import re
from .core import backup

CONFLICT_START = '<<<<<<< '
CONFLICT_MID = '======='
CONFLICT_END = '>>>>>>> '

def resolve_conflicts_in_file(path: Path):
    txt = path.read_text()
    if CONFLICT_START not in txt:
        return False
    backup(path)
    parts = re.split(r"(^<<<<<<< .*$|^=======$|^>>>>>>> .*$)", txt, flags=re.M)
    out = []
    i = 0
    n = len(parts)
    while i < n:
        seg = parts[i]
        if seg.startswith('<<<<<<< '):
            ours = parts[i+1]
            sep = parts[i+2] if i+2 < n else ''
            theirs = parts[i+3] if i+3 < n else ''
            prefer = 'ours' if not re.search(r'TODO|FIXME', ours) else 'theirs'
            out.append(ours if prefer == 'ours' else theirs)
            i += 4
        else:
            out.append(seg); i += 1
    newtxt = ''.join(out)
    path.write_text(newtxt)
    return True

def resolve_conflicts(root=Path('.')):
    results = {'checked':0, 'resolved':[]}
    for p in root.rglob('*'):
        if p.is_file() and p.suffix in ('.py','.js','.jsx','.ts','.tsx','.json','.yaml','.yml'):
            results['checked'] += 1
            ok = resolve_conflicts_in_file(p)
            if ok:
                results['resolved'].append(str(p))
    return results
