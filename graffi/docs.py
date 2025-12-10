from pathlib import Path
from .semantic import parse_python_file
from .core import backup, ensure_dir
import re, json

def suggest_docstring_for_function(fn):
    name = fn.get('name')
    args = fn.get('args', [])
    params = '\n'.join([f"- {a}: parameter" for a in args]) if args else 'None'
    return f"""{name}({', '.join(args)}) — auto-generated short description.\n\nParameters:\n{params}\n\nReturns:\n- result\n"""

def gen_docs(root=Path('.'), apply=False):
    changes = []
    for p in root.rglob('*.py'):
        parsed = parse_python_file(p)
        if not parsed or 'functions' not in parsed: continue
        src = p.read_text()
        lines = src.splitlines()
        modified = False
        for fn in parsed['functions']:
            ln = fn['lineno'] - 1
            window = '\n'.join(lines[max(0,ln-2):ln+3])
            if '"""' in window or "'''" in window:
                continue
            doc = suggest_docstring_for_function(fn)
            indent = re.match(r"(\s*)def", lines[ln]).group(1) if re.match(r"(\s*)def", lines[ln]) else '    '
            doc_block = indent + '"""' + '\n'.join(indent + ' ' + l for l in doc.splitlines()) + '\n' + indent + '"""'
            lines.insert(ln+1, doc_block)
            modified = True
        if modified:
            out = '\n'.join(lines) + '\n'
            changes.append((p, out))
            if apply:
                backup(p)
                p.write_text(out)
    # write summary
    ensure_dir(Path('.graffi_helper_model'))
    (Path('.graffi_helper_model') / 'docs_changes.json').write_text(json.dumps([str(p) for p,_ in changes], indent=2))
    return changes
