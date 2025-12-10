# graffi/agents/architecture.py
"""
Architecture agent:
- Builds import graph
- Detects circular dependencies
- Detects hotspots (high in-degree modules)
"""

from pathlib import Path
import ast
from collections import defaultdict

def _collect_imports(path: Path):
    try:
        src = path.read_text(encoding="utf-8")
    except Exception:
        return []
    try:
        tree = ast.parse(src)
    except Exception:
        return []
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return list(imports)

def build_graph(root: Path):
    graph = {}
    for py in root.rglob("*.py"):
        rel = str(py.relative_to(root))
        graph[rel] = _collect_imports(py)
    return graph

def detect_cycles(graph):
    nodes = list(graph.keys())
    index = {n:i for i,n in enumerate(nodes)}
    adj = [[] for _ in nodes]

    for n, deps in graph.items():
        i = index[n]
        for d in deps:
            for cand in nodes:
                if cand.endswith(f"{d}.py") or cand.startswith(d):
                    adj[i].append(index[cand])

    visited = [0]*len(nodes)
    cycles = []

    def dfs(u, path):
        visited[u] = 1
        path.append(u)
        for v in adj[u]:
            if visited[v] == 0:
                dfs(v, path)
            elif visited[v] == 1:
                cyc = [nodes[x] for x in path[path.index(v):]]
                cycles.append(cyc)
        path.pop()
        visited[u] = 2

    for i in range(len(nodes)):
        if visited[i] == 0:
            dfs(i, [])

    unique = []
    seen = set()
    for c in cycles:
        key = "->".join(c)
        if key not in seen:
            unique.append(c)
            seen.add(key)
    return unique

def analyze(root: str = "."):
    R = Path(root)
    graph = build_graph(R)
    cycles = detect_cycles(graph)

    indeg = defaultdict(int)
    for f, deps in graph.items():
        for d in deps:
            indeg[d] += 1

    hotspots = sorted(indeg.items(), key=lambda x: -x[1])[:10]

    return {
        "summary": {
            "python_files_scanned": len(graph),
            "cycles_found": len(cycles),
        },
        "cycles": cycles,
        "hotspots": hotspots,
        "graph_sample": {k: graph[k] for k in list(graph.keys())[:20]}
    }

