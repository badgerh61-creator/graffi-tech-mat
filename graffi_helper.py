"""
Graffi Omega Helper CLI
"""

import argparse
import json
from pathlib import Path
from graffi import semantic, docs, scaffold, updater, conflicts
from graffi import agents

def run_doctor():
    root = str(Path(".").resolve())
    report = {"time": __import__("time").asctime()}

    print("1) Generating semantic model...")
    model = semantic.build_semantic_model()
    report["python_files"] = len(model.get("python", {}))

    print("2) Checking scaffold...")
    report["scaffold"] = scaffold.scaffold_validate(fix=False)

    print("3) Evolution analysis...")
    evo = updater.analyze_evolution()
    report["evolution_file"] = str(evo)

    print("4) Running agents...")
    agent_map = {
        "architecture": agents.architecture,
        "infra": agents.infra,
        "safety": agents.safety,
        "frontend": agents.frontend,
        "backend": agents.backend,
        "evolution": agents.evolution,
        "refactor": agents.refactor,
    }

    agent_reports = {}
    for name, mod in agent_map.items():
        try:
            agent_reports[name] = mod.analyze(root)
        except Exception as e:
            agent_reports[name] = {"error": str(e)}

    report["agents"] = agent_reports

    out = Path(".graffi_helper_model") / "doctor_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print("\nDoctor report written to:", out)
    return out

# ---------------------------
# Additional CLI commands
# ---------------------------
def run_generate_refactor_patches():
    from graffi.agents import refactor
    res = refactor.generate_refactor_patches(".")
    print(json.dumps(res, indent=2))

def run_radon_report():
    from graffi.agents import refactor
    res = refactor.radon_report(".")
    print(json.dumps(res, indent=2))

def run_apply_patch(patch):
    from graffi.agents import refactor
    print(refactor.apply_patch(patch))

def run_commit_patch(patch, message):
    from graffi.agents import refactor
    print(refactor.commit_patch(patch, message=message))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=[
        "doctor",
        "regen-modules",
        "gen-docs",
        "analyze-evolution",
        "generate-refactor-patches",
        "radon-report",
        "apply-patch",
        "commit-patch",
    ])
    parser.add_argument("--patch", help="Path to a .patch file")
    parser.add_argument("--message", help="Commit message")
    args = parser.parse_args()

    if args.cmd == "doctor":
        run_doctor()
    elif args.cmd == "regen-modules":
        updater.regenerate_modules()
    elif args.cmd == "gen-docs":
        docs.gen_docs(apply=False)
    elif args.cmd == "analyze-evolution":
        updater.analyze_evolution()
    elif args.cmd == "generate-refactor-patches":
        run_generate_refactor_patches()
    elif args.cmd == "radon-report":
        run_radon_report()
    elif args.cmd == "apply-patch":
        run_apply_patch(args.patch)
    elif args.cmd == "commit-patch":
        run_commit_patch(args.patch, args.message or "graffi-helper: apply patch")

