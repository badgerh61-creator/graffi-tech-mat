from pathlib import Path
import ast, json, re
from .core import ensure_dir
MODEL_DIR = Path('.graffi_helper_model')

def parse_python_file(path: Path):
    try:
        src = path.read_text()
    except Exception:
        return {}
    try:
        tree = ast.parse(src)
    except Exception as e:
        return {'error': str(e)}
    visitor = {'functions': [], 'classes': [], 'imports': []}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            visitor['functions'].append({'name': node.name, 'lineno': node.lineno, 'args': [a.arg for a in node.args.args]})
        if isinstance(node, ast.ClassDef):
            visitor['classes'].append({'name': node.name, 'lineno': node.lineno})
        if isinstance(node, ast.Import):
            for n in node.names: visitor['imports'].append(n.name)
        if isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for n in node.names: visitor['imports'].append(module + '.' + n.name)
    return visitor

def build_semantic_model(root: Path = Path('.')):
    model = {'time': __import__('time').asctime(), 'python': {}, 'js': {}}
    for p in root.rglob('*.py'):
        rel = str(p.relative_to(root))
        model['python'][rel] = parse_python_file(p)
    js_pattern = re.compile(r"import\s+.*from\s+['\"](.*?)['\"]|require\(['\"](.*?)['\"]\)")
    for p in root.rglob('*.js'):
        try:
            t = p.read_text()
            imports = js_pattern.findall(t)
            model['js'][str(p.relative_to(root))] = {'imports': imports[:10]}
        except Exception:
            model['js'][str(p.relative_to(root))] = {'error': 'read'}
    ensure_dir(MODEL_DIR)
    (MODEL_DIR / 'semantic_model.json').write_text(json.dumps(model, indent=2))
    return model
