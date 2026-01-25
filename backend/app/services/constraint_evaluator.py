def evaluate_constraints(curves, constraints):
    """
    Stub evaluator:
    - Real solver comes later (Gauss-Newton, graph-based, etc.)
    """
    return SolveResult(
        success=True,
        solved_parameters={
            curve.id: curve.parameters | {"_solved": True}
            for curve in curves
        }
    )

